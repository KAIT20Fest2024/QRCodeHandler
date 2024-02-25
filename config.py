import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'test_secret_key_22734123'
