from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, SelectField, DecimalField
from wtforms.validators import DataRequired, Email, Length
from wtforms.widgets import TextArea
from flask_wtf.file import FileField, FileRequired, FileAllowed
# value, text
expenses = [
('Diesel', 'Diesel'),
('Petrol', 'Petrol'),
('CAR PARKING', 'CAR PARKING'),
('TOLLS', 'TOLLS'),
('AIR FARES', 'AIR FARES'),
('TRAIN FARES', 'TRAIN FARES'),
('OTHER TRAVEL', 'OTHER TRAVEL'),
('ACCOMODATION', 'ACCOMODATION'),
('SUBSISTENCE', 'SUBSISTENCE'), 
('STAFF ENTERTAINING', 'STAFF ENTERTAINING'),
('CUSTOMER ENTERTAINING', 'CUSTOMER ENTERTAINING'),
('STATIONARY', 'STATIONARY'),
('MISCELLANEOUS','MISCELLANEOUS')
]

roles = [
(1, 'Employee'),
(2, 'Manager'),
]

class SignupForm(Form):
	first_name = StringField('First Name', validators=[DataRequired("First name is required")], render_kw={'class':'form-control'})
	last_name = StringField('Last Name', validators=[DataRequired("Last name is required")], render_kw={'class':'form-control'})
	email = StringField('Email', validators=[DataRequired("Email is requried"), Email("Incorrect Email value")], render_kw={'class':'form-control', 'autocomplete':'off'})
	phone = StringField('Phone Number', validators=[DataRequired("Phone number is required")], render_kw={'class':'form-control'})
	role = SelectField('Role', choices=roles, render_kw={'class':'custom-select d-block w-100'}, coerce=int)
	password = PasswordField('Password', validators=[DataRequired("Password is required"), Length(min=8, message="Password must be at least 8 characters long")], render_kw={'class':'form-control'})
	submit = SubmitField('Sign Up')

class LoginForm(Form):
	email = StringField('Email', validators=[DataRequired("Please enter your email"), Email("Please enter your email")])
	password = PasswordField('Password', validators=[DataRequired("Password is required")])
	submit = SubmitField('Sign In')

class RequestForm(Form):
	type = SelectField(u'Expense Type', choices=expenses, render_kw={'class':'custom-select d-block w-100'})
	description = StringField('Last Name', validators=[DataRequired("Description is required")], render_kw={"placeholder": "Add Description", "rows": 8, 'class':'form-control'}, widget=TextArea())
	image = FileField(validators=[FileRequired(), FileAllowed(['jpg', 'png', 'gif'], 'Images only!')])
	amount = DecimalField('Amount', validators=[DataRequired("An amount is required")], places=2, render_kw={"placeholder": "Enter amount", "rows": 8, 'class':'form-control'})
	submit = SubmitField('Submit Request')
