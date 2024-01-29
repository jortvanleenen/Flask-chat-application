import os

# Working directory of application
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = \
        os.environ.get('SECRET_KEY') or '323e84158e412e2b9ec1e0d2da5dc2eb'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
