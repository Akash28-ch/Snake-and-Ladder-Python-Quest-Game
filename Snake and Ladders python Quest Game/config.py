import os

# Get the absolute path of the directory where this file is located
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'python-quest-secret-123'
    # Use absolute path for the database file
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'python_quest.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False