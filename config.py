import os

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    ENCRYPTION_KEY = 'scott me up beamy'

