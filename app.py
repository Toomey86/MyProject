from flask import Flask,  render_template, request, session, redirect, url_for, send_from_directory
from flask_migrate import MigrateCommand, Migrate
from models import db, User, Requests
from forms import SignupForm, LoginForm, RequestForm
from helpers.slugify import slugify
from werkzeug import secure_filename
from flask_mail import Mail, Message
import pygal

app = Flask(__name__)

POSTGRES = {
    'user': 'postgres',
    'pw': 'password',
    'db': 'blah',
    'host': 'localhost',
    'port': '5432',}
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/blah'
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s" % POSTGRES
db.init_app(app)
app.secret_key = "development-key"

# mail server not used
app.config.update(
	DEBUG=True,
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'business.expense.tracker@gmail.com',
	MAIL_PASSWORD = 'e7hDzBKx2dSXzQ5'
	)

#EMAIL SETTINGS
# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USERNAME'] = 'Martin.Toomey86@gmail.com'
# app.config['MAIL_PASSWORD'] = ''
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = True

mail = Mail(app)


# Template Filters
@app.template_filter('slugify')
def _slugify(string):
    if not string:
        return ""
    return None

# @app.route('/send-mail/')
# def send_mail():
# 	try:
#         msg = Message("Forgot Password?",
#             sender="business.expense.tracker@gmail.com",
#             recipients=[email])
#         msg.body = 'Hello '+username+',\nYou or someone else has requested that a new password be generated for your account. If you made this request, then please follow this link:'+link
#         msg.html = render_template('/mails/reset-password.html', username=username, link=link)
#         mail.send(msg)
# 		return 'Mail sent!'
# 	except Exception as e:
# 		return(str(e))


@app.route("/export")
def export():
    try:
        bar_chart = pygal.Bar()     # Then create a bar graph object
        bar_chart.add('Fibonacci', [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55])  # Add some values
        #bar_chart.render_to_file('bar_chart.svg')  # Save the svg to a file
        chart_data = bar_chart.render_data_uri() # saves to embedd tag
        #return bar_chart.render_response()
        return render_template("export.html",chart_data=chart_data)
    except Exception as e:
        return(str(e))


@app.route("/logout")
def logout():
    session.pop('email', None)
    session.pop('uid', None)
    return redirect(url_for("login"))
    #return render_template("login.html")

@app.route("/", methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def login():
    if 'uid' in session:
        return redirect(url_for('dashboard'))

    form = LoginForm()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template("login.html", form=form)
        else:
            email = form.email.data
            password = form.password.data
            user = User.query.filter_by(email=email).first()
            print("user")
            if user is not None and user.check_password(password):
                session['email'] = user.email
                session['uid'] = user.uid
                return redirect(url_for('dashboard'))
            else:
                return redirect(url_for('login'))

    elif request.method == 'GET':
        return render_template("login.html", form=form)


@app.route("/profile", methods=['GET'])
def profile():
    if 'uid' not in session:
        return redirect(url_for('login'))
    user = User.query.filter_by(uid=session['uid']).first()

    # msg = Message('Hello', sender = 'sidarcy@gmail.com', recipients = ['sidarcy@gmail.com'])
    #   	msg.body = "Your profile has been viewed"
    #   	mail.send(msg)
    return redirect(url_for('profile'))
    #return render_template("profile.html", user=user)


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    # you need to be an admin to create new accounts
    if 'uid' not in session:
        return redirect(url_for('dashboard'))
    form = SignupForm()

    currentUser = User.query.filter_by(uid=session['uid']).first()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template("signup.html", form=form, user=currentUser)
        else:
            newuser = User(firstname=form.first_name.data,
                           lastname=form.last_name.data,
                           email=form.email.data,
                           phone=form.phone.data,
                           password=form.password.data,
                           manager_id=currentUser.uid,
                           manager=[currentUser],
                           role=form.role.data)
            db.session.add(newuser)
            db.session.commit()
            return redirect(url_for("users"))
    elif request.method == 'GET':
        return render_template("signup.html", form=form, user=currentUser)

@app.route("/dashboard")
def dashboard():
    if 'uid' not in session:
        return redirect(url_for('login'))
    currentUser = User.query.filter_by(uid=session['uid']).first()
    return render_template("dashboard.html", user=currentUser, request=request)


@app.route("/users")
def users():
    if 'uid' not in session:
        return redirect(url_for('login'))
    currentUser = User.query.filter_by(uid=session['uid']).first()

    return render_template("employees.html", user=currentUser)


@app.route("/employee-requests")
def employee_requests():
    if 'uid' not in session:
        return redirect(url_for('login'))
    currentUser = User.query.filter_by(uid=session['uid']).first()

    requests = None

    if currentUser.role == 0:
        requests = Requests.query.filter(Requests.status.in_(('Awaiting', 'Awaiting Finance'))).all()

    elif currentUser.role == 2:
        # Filter requests so as only to show awaiting one
        for employee in currentUser.employees:
            employee.requests = [i for i in employee.requests if i.status == 'Awaiting']
    else:
        return "Not Authorized"

    return render_template("employee-requests.html", user=currentUser, requests=requests)


@app.route("/new", methods=['GET', 'POST'])
def newrequest():
    if 'uid' not in session:
        return redirect(url_for('login'))
    form = RequestForm()

    currentUser = User.query.filter_by(uid=session['uid']).first()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template("request.html", form=form)
        else:

            filename = secure_filename(form.image.data.filename)
            file_extention = filename.split('.')[1]

            req = Requests(type=form.type.data,
                           description=form.description.data,
                           status='Awaiting',
                           image=file_extention,
                           amount=form.amount.data,
                           user=currentUser)
            db.session.add(req)
            db.session.commit()

            # Save image to disk
            unique_filename = "%s.%s" % (req.id, file_extention)
            form.image.data.save('uploads/' + unique_filename)

            return redirect(url_for('dashboard'))
    elif request.method == 'GET':
        return render_template("request.html", form=form, user=currentUser)


@app.route('/view/<int:request_id>')
def viewrequest(request_id):
    currentUser = User.query.filter_by(uid=session['uid']).first()
    req = Requests.query.filter_by(id=request_id).first()
    if req is not None:
        return render_template("view.html", req=req, user=currentUser)
    else:
        return "404"


@app.route("/approve", methods=['POST'])
def approve():
    currentUser = User.query.filter_by(uid=session['uid']).first()
    # get id
    request_id = request.form['id']

    req = Requests.query.filter_by(id=request_id).first()

    if currentUser.role == 2:
        req.status = "Awaiting Finance"
    elif currentUser.role == 0:
        req.status = "Approved"
    db.session.commit()

    return redirect(url_for('employee_requests'))


@app.route("/reject", methods=['POST'])
def reject():
    currentUser = User.query.filter_by(uid=session['uid']).first()
    # get id
    request_id = request.form['id']
    req = Requests.query.filter_by(id=request_id).first()
    req.status = "Declined"
    db.session.commit()
    # SEND EMAIL HERE
    return redirect(url_for('employee_requests'))


@app.route('/uploads/<path:path>')
def view_(path):
    return send_from_directory('uploads', path)

@app.route('/tcs')
def tcs():
    #return render_template('tcs.html')
    return redirect(url_for("tcs"))

@app.route('/license')
def license():
    #return render_template('license.html')
    return redirect(url_for("license"))

@app.route('/privacy_policy')
def privacy_policy():
    #return render_template('privacy_policy.html')
    return redirect(url_for("privacy_policy"))

@app.route('/faq')
def faq():
    #return render_template('faq.html')
    return redirect(url_for("faq"))

@app.route('/settings')
def settings():
    #return render_template('settings.html')
    return redirect(url_for("settings"))


if __name__ == "__main__":
    app.run(debug=True)
#
