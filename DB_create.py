from models import db, User, Requests
#from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import User


# FLASK_APP(app.py)
#app = Flask(__name__)
db.create_all()
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/blah'
admin = User(firstname='Martin', lastname='Toomey', email='martin.toomey86@gmail.com', phone='0879126382', role=0,manager_id=2, manager=None, password='password')
admin2 = User(firstname='Alison', lastname='Toomey', email='allymkm@gmail.com', phone='0857864940', role=0,manager_id=1, manager=None, password='password')

db.session.add(admin)
db.session.add(admin2)
db.session.commit()
#db.init_app(app)
#app.secret_key = "development-key"
#db = SQLAlchemy(app)
# Migrate(app,db)
