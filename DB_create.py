from app import db
from models import User
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# FLASK_APP(app.py)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/blah'
db.init_app(app)
app.secret_key = "development-key"
db = SQLAlchemy(app)
Migrate(app,db)


db.create_all()
admin = User(firstname='Martin', lastname='Toomey', email='martin.toomey86@gmail.com', phone='0879126382', role=0,manager_id=None, manager=None, password='password')
db.session.add(admin)
db.session.commit()
