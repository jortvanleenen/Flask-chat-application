from flask import Flask
from flask_wtf.csrf import CSRFProtect

from config import Config

from flask_sqlalchemy import SQLAlchemy
from flask_argon2 import Argon2
from flask_login import LoginManager
from flask_socketio import SocketIO
import logging
from logging.handlers import RotatingFileHandler
import os

# Define dependencies required for the application
db = SQLAlchemy()
argon2 = Argon2()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message_category = 'info'
socketio = SocketIO()
csrf = CSRFProtect()


def create_app():
    # Create an instance of the application
    app = Flask(__name__)
    # Set all Flask-related settings (see '/config.py')
    app.config.from_object(Config)
    # Initialise dependencies with current application instance
    db.init_app(app)
    argon2.init_app(app)
    login.init_app(app)
    socketio.init_app(app)
    csrf.init_app(app)
    # Register blueprints
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    # Make use of logging during production for current application instance
    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240,
                                           backupCount=5)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)

    return app


from app import models
