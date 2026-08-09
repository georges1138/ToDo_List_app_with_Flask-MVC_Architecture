import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'your_unique_secret_key'

    SQLALCHEMY_DATABASE_URI = (
            'sqlite:///' + os.path.join(basedir, 'data.db')
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
