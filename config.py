#default config
import os
class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = "development-key"
    POSTGRES = {
        'user': 'postgres',
        'pw': 'password',
        'db': 'blah',
        'host': 'localhost',
        'port': '5432',}
    basedir = os.path.abspath(os.path.dirname(__file__)) #absalout path to help when moving to different os
    #a modulwe is loaded in python this file var is built in and is set name of the file
    #SQLALCHEMY_DATABASE_URI = "postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s" % POSTGRES
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://' + \
    os.path.join(basedir, "postgres:password@localhost/blah")
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(BaseConfig):
    DEBUG = True

class ProductionConfig(BaseConfig):
        DEBUG = False
