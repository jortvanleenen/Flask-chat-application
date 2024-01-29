from datetime import datetime, timedelta

from flask import redirect, render_template, flash, url_for, jsonify, request, Response
from flask_login import current_user, login_required
from sqlalchemy import asc

from app import db
from app.main import bp
from app.chatting import create_chat
from app.main.forms import chat_form_builder, MessageForm
from app.models import User, Chat, Message


@bp.before_request
def before_request() -> None:
    """Keep track of active users."""
    if current_user.is_authenticated:
        current_user.last_active = datetime.utcnow()
        db.session.commit()


@bp.route('/')
def index():
    """Navigate all traffic from the root to appropriate pages."""
    if current_user.is_authenticated:
        return redirect(url_for('main.chat_screen'))
    else:
        return redirect(url_for('auth.login'))


@bp.route('/chat', methods=['GET', 'POST'])
@login_required
def chat_screen():
    """Handle the chat screen.

    GET-requests result in chat_screen.html being returned to the client. POST-
    requests expect the dynamic ChatForm to be serialized.
    """
    filter_after = datetime.utcnow() - timedelta(minutes=5)
    active_users = User.query. \
        filter(User.last_active >= filter_after,
               User.username != current_user.username).all()

    message_form = MessageForm()
    chat_form = chat_form_builder(active_users)

    # If checked with the regular validate_on_submit-function, message_form
    # can match as well
    if chat_form.open.data:
        if chat_form.validate():
            db.session.add(create_chat(current_user.username, chat_form))
            db.session.commit()
        else:
            flash('At least one user needs to be selected.', 'danger')
        return redirect(url_for('main.chat_screen'))

    return render_template('chat_screen.html', title='Chat',
                           active_users=active_users, chat_form=chat_form,
                           message_form=message_form, chats=current_user.chats)


@bp.route('/open-chat', methods=['POST'])
@login_required
def open_chat() -> Response:
    """Handle chat opening through AJAX-calls."""
    chat_id = request.form['chat_id']
    chat = Chat.query.filter(Chat.chat_id == chat_id,
                             Chat.users.contains(current_user)).first()
    response = {'status': 'fail'}
    if chat:
        messages = chat.messages.order_by(asc(Message.sent_timestamp)).all()
        response_messages = []
        for message in messages:
            response_messages.append([message.sender_username,
                                      str(message.sent_timestamp),
                                      message.content])
        response.update([('messages', response_messages),
                         ('status', 'success'),
                         ('chat_id', chat_id),
                         ('current_user', current_user.username)])
    return jsonify(response)


@bp.route('/send-message', methods=['POST'])
@login_required
def send_message() -> Response:
    """Handle message sending through AJAX-calls."""
    response = {'status': 'fail'}
    message_form = MessageForm()
    # Form was fully submitted through POST-request, thus can be validated below
    if message_form.validate_on_submit():
        chat_id = message_form.chat_id.data
        if current_user.in_chat(chat_id):
            message = Message(content=message_form.content.data,
                              sender_username=current_user.username,
                              chat_id=chat_id)
            db.session.add(message)
            db.session.commit()
            response_message = ([[message.sender_username,
                                  str(message.sent_timestamp),
                                  message.content]])
            # Note the double set, as displayMessages() expects multiple
            # message objects ([ts1, cont1, user1], [ts2, cont2, user2]])
            response.update([('messages', response_message),
                             ('status', 'success'),
                             ('chat_id', chat_id)])
    return jsonify(response)
