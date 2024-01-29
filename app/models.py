from datetime import datetime
from flask_login import UserMixin
from app import argon2, db, login

participatesIn = db.Table('participatesIn',
                          db.Column('user_username',
                                    db.String(64),
                                    db.ForeignKey('user.username')),
                          db.Column('chat_id',
                                    db.Integer,
                                    db.ForeignKey('chat.chat_id')))


class User(UserMixin, db.Model):
    """Model for the application user."""
    username = db.Column(db.String(64), primary_key=True)
    password_hash = db.Column(db.String(128), nullable=False)
    last_active = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    sent_messages = db.relationship('Message', backref='sender', lazy='dynamic')
    chats = db.relationship('Chat', secondary=participatesIn, lazy='dynamic',
                            backref=db.backref('users', lazy='dynamic'))

    def __repr__(self) -> str:
        return f"User({self.username})"

    def set_password(self, password) -> None:
        """Convert password to hash and set for the user."""
        self.password_hash = argon2.generate_password_hash(password)

    def check_password(self, password) -> bool:
        """Convert password to hash and check for the user."""
        return argon2.check_password_hash(self.password_hash, password)

    def in_chat(self, chat_id) -> bool:
        """Check if user is a participant of given chat."""
        return bool(Chat.query.filter(Chat.chat_id == chat_id,
                                      Chat.users.contains(self)).first())

    # Overrides from mixin as it defaults to 'id'
    def get_id(self) -> str:
        return str(self.username)


@login.user_loader
def load_user(username):
    return User.query.get(username)


class Chat(db.Model):
    """Model for a chat."""
    chat_id = db.Column(db.Integer, primary_key=True)
    messages = db.relationship('Message', backref='chat', lazy='dynamic')

    def __repr__(self) -> str:
        return f"Chat({self.chat_id})"


class Message(db.Model):
    """Model for a chat message."""
    message_id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(256), nullable=False)
    sent_timestamp = db.Column(db.DateTime, index=True, nullable=False,
                               default=datetime.utcnow)
    sender_username = db.Column(db.String(64), db.ForeignKey('user.username'),
                                nullable=False)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.chat_id'),
                        nullable=False)

    def __repr__(self) -> str:
        return f"Message({self.content})"
