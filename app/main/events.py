from flask import session
from flask_login import login_required, current_user
from flask_socketio import leave_room, emit, join_room

from app import socketio


@socketio.on('join_chat')
@login_required
def join_chat(json) -> None:
    """Handle Socket.IO room joining and leaving.

    Handles Socket.IO room joining and leaving based on the user's session.
    Keyword arguments:
    json - a JSON-formatted object with at least the chat_id of the wished room
    """
    chat_id = json['chat_id']
    if current_user.in_chat(chat_id):
        if 'room' in session:
            leave_room(session['room'])
        join_room(chat_id)
        session['room'] = chat_id


@socketio.on('send_message')
@login_required
def new_message(json) -> None:
    """Handle Socket.IO room messaging.

    Handles Socket.IO room messaging by emitting new messages to all within
    a certain chat.

    Keyword arguments:
    json - a JSON-formatted object with at least the chat_id and messages
    """
    chat_id = json['chat_id']
    if current_user.in_chat(chat_id):
        emit('new_message', {'messages': json['messages']}, room=chat_id)
