<!-- PREREQUISITES: -->

Download: https://www.pgadmin.org/
Sign up for https://www.heroku.com/ and download the toolbelt
Github account
e7hDzBKx2dSXzQ5

<!--- Python Libraries used -->
pip install vitual env
pip install flask_sqlalchemy  For DB models
pip install flask_migrate
pip install flask_wtf # for forms
pip install psycopg2  # for python/postgre
pip install flask_migrate
pip install FLask-Mail # for email
pip install pygal
pip install gunicorn


<!-- TECHNOLOGY USED -->
Flask
Postgres DB
Bootstrap for font end
JS and css


<!--- VIRTUAL ENVIROMENT SETUP -->
<!-- MAC/Linux -->
To create a virtual env: "virtualenv venv"
To activte virtual env: "source venv3.6/bin/activate"

apt-get install python3-venv
python3 -m venv /path/to/new/virtual/environment
virtualenv venv3.6
source venv3.6/bin/activate
pip install -r reqs.txt

<!-- Windows need conda installed -->
conda create -n MyTestEnv
conda env list # list of Enviroments
activate myflaskenv
deactivate
source deactivate # Mac
conda env list
conda remove --name myenv --all


<!-- DATABASE INFO -->

PGAdmin: http://127.0.0.1:58678/browser/
digital ocean ip: 178.128.174.253
                  206.189.25.70


NokieN900 DB password

<!--  Query to create the master user in PGAdmin -->

INSERT INTO users (firstname, lastname, email, pwdhash)
VALUES ('Martin', 'Toomey', 'martin.toomey86@gmail.com', 'pbkdf2:sha256:50000$nvJQzJD8$2dcd0b5756f000e070f7036832d6fd1f08a5a24919d5003065eb50aa211d77fa');

<!-- RUNNNG APPLICIATION -->

$ export FLASK_APP=app
$ flask run

or simply use:

$ python app.py



<!--GitHub setup  -->
git init
git add README.md
git add .
git commit -m "first commit"
git remote add origin https://github.com/Toomey86/MyProject.git

git push --set-upstream origin amend-my-name

git push -u origin master

#login Toomey86
#Password: l83item


<!--Create a requirment.txt file  -->
pip freeze > requirements.txt

<!--Heroku set up  -->
sudo snap install --classic heroku  #ubuntu
heroku login or heroku login -i for cli
git init
heroku git:remote -a business-expense-tracker
or testherokuenv-postgres
git add .
git commit -am "Some message about changes"
git push heroku master
<!--Other Heroku useful commands  -->
heroku config:set APP_SETTINGS=config.productionConfig --remote heroku
heroku pg:promote HEROKU_POSTGRESQL_RED_URL

heroku open
heroku ps
heroku ps:scale web=1

heroku addons
heroku addons:create heroku-postgresql:hobby-dev
heroku plugins:install heroku-pg-extras

heroku config | grep HEROKU_POST
heroku logs --tail #logs
heroku run python
heroku pg:reset DATABASE
heroku run rake db:migrate
heroku addons:destroy HEROKU_POSTGRESQL_<COLOR>

<!--proc file  -->
web: gunicorn app.wsgi --log-file -
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


username = doadmin
password = gyv8elr7ejd4sy11
host = db-postgresql-lon1-12053-do-user-4995347-0.db.ondigitalocean.com
port = 25060
database = defaultdb
sslmode = require


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


Manager
managerTest@gmail.com   testpassword


Employee
allymkm@gmail.com
Martin.toomey86@gmail.com


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
