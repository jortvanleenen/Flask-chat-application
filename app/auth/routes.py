from datetime import datetime, timedelta

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm
from app.models import User


@bp.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration.

    GET-requests result in register.html being returned to the client. POST-
    requests expect the RegistrationForm to be serialized.
    """
    if current_user.is_authenticated:
        flash('You were already authenticated and, therefore, have been '
              'redirected to the chat window.', 'info')
        return redirect(url_for('main.chat_screen'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # noinspection PyArgumentList
        user = User(username=str(form.username.data).lower())
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash(f'{form.username.data}, you have successfully registered'
              f' and have been automatically logged in.', 'success')
        return redirect(url_for('main.chat_screen'))
    return render_template('auth/register.html', title='Register', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user log in.

    GET-requests result in login.html being returned to the client. POST-
    requests expect the LoginForm to be serialized.
    """
    if current_user.is_authenticated:
        flash('You were already authenticated and, therefore, have been '
              'redirected to the chat window.', 'info')
        return redirect(url_for('main.chat_screen'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('main.chat_screen')
            return redirect(next_page)
        flash('Invalid username or password, please try again.', 'danger')
    return render_template('auth/login.html', title='Log in', form=form)


@bp.route('/logout')
@login_required
def logout():
    """Log a logged in user out."""
    current_user.last_active = datetime.utcnow() - timedelta(minutes=5)
    db.session.commit()
    logout_user()
    flash('You have successfully been logged out.', 'success')
    return redirect(url_for('auth.login'))
