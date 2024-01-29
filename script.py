from app import create_app, db

app = create_app()
app.app_context().push()

open('app.db', 'a').close()

db.create_all()
