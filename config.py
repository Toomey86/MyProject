#default config
import os


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = "development-key"
    #b'\xbd\x1a\x99\x1b#\xcc\xb0j\xd7Y\xb5\xaf\x12\x9d\x80\x93\x13\x02!i\xf3\x97(\xfbd\xbe\xce\xe1\x8fD\xa4\xa7'

    basedir = os.path.abspath(os.path.dirname(__file__)) #absalout path to help when moving to different os
    #a modulwe is loaded in python this file var is built in and is set name of the file
    #SQLALCHEMY_DATABASE_URI = "postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s" % POSTGRES
    HEROKU_POSTGRESQL_ROSE_URL = "postgres://nfopxizqefgzxi:15b5b42c39d97e880ab5645ad30347e10876fb013b7c08be215160701fe627d6@ec2-54-247-70-127.eu-west-1.compute.amazonaws.com:5432/d20g1bp8eg5cpl"
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://' + os.path.join(basedir, "postgres:password@localhost/blah")
    DATABASE_URI = os.environ["DATABASE_URL"] # database production
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(BaseConfig):
    DEBUG = True

class ProductionConfig(BaseConfig):
        DEBUG = False
