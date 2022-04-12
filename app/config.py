import os
class Config(object):
    SECRET_KEY = 'my_secret_key'

class DevelopmentConfig(Config):
    DEBUG = True
    ENV='development'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost/db_quetzal_coffee'
    SECURITY_PASSWORD_SALT = 'thisissecretsalt'
    
