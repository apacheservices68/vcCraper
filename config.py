import os
from dotenv import load_dotenv

load_dotenv()


class Config(object):
    # PORT = 3306
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_BINDS = {
        'db2': os.environ.get("SQLALCHEMY_DATABASE_TTCT")
    }


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
