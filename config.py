import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'test_secret_key_22734123'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or 'postgresql://postgres:postgres@localhost:5432/kait20fest'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
