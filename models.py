from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
#import db from __init__.py

db = SQLAlchemy()

# Role
# 0 is admin, 1 is manager, 2 is employee

class User(db.Model):
	__tablename__ = 'users'
	uid = db.Column(db.Integer, primary_key=True)
	firstname = db.Column(db.String(100))
	lastname = db.Column(db.String(100))
	email = db.Column(db.String(100), unique=True)
	phone = db.Column(db.String(100))
	pwdhash = db.Column(db.String(250))
	role = db.Column(db.Integer)

	employees=db.relationship('User', backref=db.backref('parent', remote_side=[uid]))
	manager_id=db.Column(db.Integer, db.ForeignKey('users.uid'))

	requests = db.relationship('Requests', backref='users', lazy=True)

	def __init__(self, firstname, lastname, email, phone, password, role, manager_id, manager):
		self.firstname = firstname.title()
		self.lastname = lastname.title()
		self.email = email.lower()
		self.phone = phone
		self.role = role
		self.set_password(password)
		self.manager_id = manager_id
		self.manager = manager


	def set_password(self, password):
		self.pwdhash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.pwdhash, password)

	def is_admin(self):
		return (self.role == 0)

	def is_manager(self):
		return (self.role == 2)

	def __repr__(self):
		return '<User %r>' % self.firstname

	def json(self):
		return {column: value if not isinstance(value, datetime.date) else value.strftime('%Y-%m-%d')
		for column, value in self._to_dict().items()}


class Requests(db.Model):
	__tablename__ = 'requests'
	id = db.Column(db.Integer, primary_key=True)
	uid = db.Column(db.Integer, db.ForeignKey('users.uid'))
	type = db.Column(db.String(100))
	description = db.Column(db.String(100))
	status = db.Column(db.String(100))
	image = db.Column(db.String(250))
	amount = db.Column(db.Float)

	user = db.relationship('User')

	def __init__(self, type, description, status, image, amount, user):
		self.type = type
		self.description = description
		self.status = status
		self.image = image
		self.amount = amount
		self.user =  user

	def __repr__(self):
		#return '<Requests %r>' % self.type
		return '%s(%s)' % (self.__class__.__name__, {
            column: value
            for column, value in self._to_dict().items()
        })
