import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:12345678@localhost:5432/rekomendasi_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'capstone-secret-key'
