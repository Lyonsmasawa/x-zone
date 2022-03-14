import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://moringa:passdb@localhost/blog'
    MAIL_SERVER = 'smtp.googlemail.com' #smtp server
    MAIL_PORT = 587 #gmail smtp server port
    MAIL_USE_TLS = True #enables a transport layer security to secure emails when sending

class ProdConfig(Config):
    pass

class TestConfig(Config):
    pass

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://moringa:passdb@localhost/blog'
    DEBUG = True

config_options = {
    'development': DevConfig,
    'production': ProdConfig,
    'test': TestConfig
}