import os

class Config(object):
    SECRET_KEY = 'stable'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://owner:owner@localhost/stable')
    SQLALCHEMY_TRACK_MODIFICATIONS = False