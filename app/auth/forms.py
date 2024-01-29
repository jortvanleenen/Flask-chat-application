from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError
from app.models import User


class RegistrationForm(FlaskForm):
    """A registration form used to register users."""
    username = StringField('Username', validators=[DataRequired(),
                                                   Length(min=2, max=64)])
    password = PasswordField('Password', validators=[DataRequired(),
                                                     Length(min=8, max=128)])
    confirm_password = \
        PasswordField('Confirm Password',
                      validators=[DataRequired(),
                                  EqualTo('password',
                                          message='The passwords were not '
                                                  'equal to each other.'),
                                  Length(min=8)])
    submit = SubmitField('Sign Up')

    # noinspection PyMethodMayBeStatic
    def validate_username(self, username):
        user = User.query.filter_by(username=str(username.data).lower()).first()
        if user is not None:
            raise ValidationError('That username is already taken. Please '
                                  'choose a different one.')


class LoginForm(FlaskForm):
    """A login form used to log users in."""
    username = StringField('Username', validators=[DataRequired(),
                                                   Length(max=64)])
    password = PasswordField('Password', validators=[DataRequired(),
                                                     Length(max=128)])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log in')
