# config.py

import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Database configuration
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'CortevaDB.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

