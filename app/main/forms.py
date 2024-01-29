from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, BooleanField, HiddenField
from wtforms.validators import DataRequired, Length, ValidationError

from app.models import User, Chat


class MessageForm(FlaskForm):
    """A message form used to send messages."""
    chat_id = HiddenField(validators=[DataRequired()])
    content = TextAreaField('Message', validators=[DataRequired(),
                                                   Length(max=256)])
    send = SubmitField('Send')

    # noinspection PyMethodMayBeStatic
    def validate_chat_id(self, chat_id):
        """Validate chat_id based on database validity."""
        chat = Chat.query.filter_by(chat_id=chat_id.data).first()
        if chat is None:
            raise ValidationError('A chat with that id does not exist!')


class ChatFormBase(FlaskForm):
    """Base class for the chat form.

    A base class for the chat form was required as it had to generate
     dynamically, due to the number of users within the form not being fixed.
    """
    open = SubmitField('Open chat')

    # Overrides default validation method to allow form-wide custom validation
    def validate(self, extra_validators=None) -> bool:
        if super().validate(extra_validators):
            # Gets all users that have been set to True
            filtered = {k for (k, v) in self.data.items() if
                        (k != 'open' and k != 'csrf_token' and v is True)}
            # Checks whether all received users exist in the database
            in_database = {user for user in filtered if
                           User.query.filter_by(username=user).first()}
            return bool(in_database)


def chat_form_builder(users):
    """Build a dynamic chat form."""

    class ChatForm(ChatFormBase):
        """Dynamic chat form based upon the ChatFormBase-class."""
        pass

    for user in users:
        setattr(ChatForm, f'{user.username}',
                BooleanField(label=f'{user.username}'))

    return ChatForm()
