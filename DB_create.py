from app import db
from models import User
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

set FLASK_APP=app.py

db.create_all()

admin = User(firstname='Martin', lastname='Toomey', email='martin.toomey86@gmail.com', phone='0879126382', role=0,manager_id=None, manager=None, password='password')
db.session.add(admin)

db.session.commit()
