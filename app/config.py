import os
import re

class Config(object):
    # uri = os.getenv("DATABASE_URL")
    # if uri.startswith("postgres://"):
    #     uri = uri.replace("postgres://", "postgresql://", 1)
    SECRET_KEY = 'stable'
    SQLALCHEMY_DATABASE_URI =  'postgresql://owner:owner@localhost/stable'#os.environ.get(uri, 'postgresql://owner:owner@localhost/stable')
    SQLALCHEMY_TRACK_MODIFICATIONS = False