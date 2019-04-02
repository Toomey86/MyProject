db = SQLAlchemy()
db.app = app
app.app_context().push()
db.init_app(app)
