

<!-- PREREQUISITES: -->

Download: https://www.pgadmin.org/
Sign up for https://www.heroku.com/ and download the toolbelt
Github account

<!--- Python Libraries used -->

vitual env
pip install Flask SQL Alchemy (For DB models)
pip install Forms WTF (for forms)
pip install FLask-Mail (email)

<!-- TECHNOLOGY USED -->

Flask
Postgres DB
Bootstrap for font end
Vanilla JS ans css


<!--- VIRTUAL ENVIROMENT SETUP -->
To create a virtual env: "virtualenv venv"
To activte virtual env: "source venv/bin/activate"

<!-- DATABASE INFO -->

PGAdmin: http://127.0.0.1:58678/browser/

NokieN900 DB password

<!--  Query to create the master user in PGAdmin -->

INSERT INTO users (firstname, lastname, email, pwdhash)
VALUES ('Martin', 'Toomey', 'martin.toomey86@gmail.com', 'pbkdf2:sha256:50000$nvJQzJD8$2dcd0b5756f000e070f7036832d6fd1f08a5a24919d5003065eb50aa211d77fa');

<!-- RUNNNG APPLICIATION -->

$ export FLASK_APP=app
$ flask run

or simply use:

$ python app.py

<!--Heroku set up  -->


<!-- Shell -->
$ flask shell
from models import db
db.create_all()

<!--- Create new user -->
from models import User
admin = User(firstname='Martin', lastname='Toomey', email='martin.toomey86@gmail.com', phone='0879126382', role=0,manager_id=None, manager=None, password='password')
db.session.add(admin)
db.session.commit()

<!-- If running into issues use:  -->
db.session.rollback()


<!-- ORM Queries -->
User.query.all();


<!-- APP STORYBOARD --->

--  Employee flow --

User is introduced to a login screen (/login)
They log in and are brought to a dashbopard containin all their expensesis (Active, denies and approved) (/dashboard)

User can click on a previous request (/request)
User can create a new request (/new)


-- Manager user flow --

Manger is introduced to a login screen
Manger logs in and is greeted with their dashboard containing a list of requests.
Manger can view each request (/review)
Manger can approve/deny a request (/review)


-- Financial user flow --

login
list off all waiting expenses
approve
generate report


<!-- URLS -->

http://127.0.0.1:5000/

/
/dashboard
/new
/view
/


Software development lifecycle

https://raygun.com/blog/software-development-life-cycle/

1. Planning
2. Requiements
3. Design and prototyping (do some sketchs etc)
4. Software Development
5. Testing (UAT)
6. Deployment (Heroku)
7. Operations & Mainteanance (iterations, releases, rince & repeat)

MVC pattern https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller

The Request Response loop

// sample users

Financial Admin
sdarcy@cartrawler.com
NokaiN900

Manager
john@himself.com
NokiaN900

Employee
ally@expenses.com
Martin


Todo

Pub date and order by such
Emails (notifications)

Delete expense (canceled status?)
Delete users

Add reason for rejection
Loop user back to manager


Add to git
Heroku setup and deploy


Better floating off numbers
Allow users to update profile (2. User Authentication)
Draft expenses (2.) - not required

Generate reports (Finance admin)
View expenses by filter (Monthly yearly 2.)

Approvers (2.5.)
Policies
Cache main user
Expense type as new table (admin can add, see 3.1)
Change statuses to a DB table?
Add receipt



Notes & Questions

Are adding, submitting and send for approval all different steps

Is a location required as part of the expense

Is the line manager / finance admin not the approver?

Cost center appears in the Entity but no where else?

Is there a need to a notification DB table?
