from setuptools import setup

setup(name='flask-chat-application',
      version='1.0.0',
      description='Flask chat application',
      url='https://github.com/jortvanleenen/Flask-chat-application',
      author='Jort van Leenen',
      author_email='jort@vleenen.nl',
      packages=['app', 'app.auth', 'app.main', 'app.errors'],
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Framework :: Flask',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Natural Language :: English',
          'Programming Language :: Python :: 3',
          'Topic :: Communications :: Chat',
          'Private :: Do Not Upload',
      ],
      install_requires=[
          "Flask~=2.1.1",
          "Flask-Argon2~=0.2.0.0",
          "Flask-Login~=0.6.0",
          "Flask-SocketIO~=5.1.1",
          "Flask-SQLAlchemy~=2.5.1",
          "Flask-WTF~=1.0.1",
          "setuptools~=62.1.0"
      ])
