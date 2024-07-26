# config.py
import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'mysql+pymysql://root:199623/@localhost:3306/gestion_campesina_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

