import os

class Config:
    SECRET_KEY = 'Flask'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://louise:demy@localhost/pitches'

class ProdConfig(Config):
    pass


class DevConfig(Config):
    DEBUG = True

config_options = {
'development':DevConfig,
'production':ProdConfig
}