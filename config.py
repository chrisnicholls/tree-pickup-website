import os
MYSQL_DATABASE_USER = 'scoutsUser'
MYSQL_DATABASE_PASSWORD = 'scoutsPass'
MYSQL_DATABASE_DB = 'scouts'
MYSQL_DATABASE_HOST = 'localhost'
ENCRYPTION_KEY = 'scott me up beamy'


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    ENCRYPTION_KEY = 'scott me up beamy'

