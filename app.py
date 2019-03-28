from flask import Flask, render_template, request, session, redirect, url_for, send_from_directory
from models import db, User, Requests
from forms import SignupForm, LoginForm, RequestForm
from helpers.slugify import slugify
from werkzeug import secure_filename
from flask_mail import Mail, Message

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/blah'
db.init_app(app)

app.secret_key = "development-key"

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'MTOOMEY@gmail.com'
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


# Template Filters
@app.template_filter('slugify')
def _slugify(string):
    if not string:
        return ""
    return None

# end template filters

@app.route("/logout")
def logout():
    session.pop('email', None)
    session.pop('uid', None)
    return redirect(url_for("login"))


@app.route("/", methods=['GET', 'POST'])
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

    return render_template("profile.html", user=user)


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
    return render_template('tcs.html')
@app.route('/license')
def license():
    return render_template('license.html')

@app.route('/privacy_policy')
def privacy_policy():
    return render_template('privacy_policy.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')


if __name__ == "__main__":
    app.run(debug=True)
