class Configuration(object):
    DEBUG = True
    SQL_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:serafim17Varvar@localhost/items'
    SECRET_KEY = 'qwerty'

    SECURITY_PASSWORD_SALT = 'salt'
    SECURITY_PASSWORD_HASH = 'sha512_crypt'
