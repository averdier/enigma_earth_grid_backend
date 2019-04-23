# coding: utf-8

import os
from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler

basedir = Path(__file__).parent


class Config:
    NAME = os.environ.get('NAME', 'arduino_api')
    ADMINS = os.environ.get('ADMINS', '').split(',')

    AUTH_PRIVATE_KEY = os.environ.get(
        'AUTH_PRIVATE_KEY',
        str(basedir / 'docker' / 'keys' / 'auth_privkey.pem')
    )
    AUTH_PUBLIC_KEY = os.environ.get(
        'AUTH_PUBLIC_KEY',
        str(basedir / 'docker' / 'keys' / 'auth_pubkey.pem')
    )
    AUTH_AUDIENCE = os.environ.get('AUTH_AUDIENCE', 'arduino_mqtt')

    DB_USER = os.environ.get('DB_USER', 'postgres')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'example')
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_DATABASE = os.environ.get('DB_DATABASE', 'arduino_api')

    SQLALCHEMY_DATABASE_URI = 'postgres://{0}:{1}@{2}/{3}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_DATABASE)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    LOG_PATH = os.environ.get(
        'LOG_PATH',
        str(basedir / 'docker' / 'logs' / 'arduino_api.log')
    )
    LOG_SIZE = int(os.environ.get('LOG_SIZE', '20000'))
    LOG_COUNT = int(os.environ.get('LOG_COUNT', '10'))
    LOG_ENCODING = os.environ.get('LOG_ENCODING', 'utf-8')

    RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
    RESTPLUS_VALIDATE = True
    RESTPLUS_MASK_SWAGGER = False
    RESTPLUS_ERROR_404_HELP = True
    JSON_SORT_KEYS = False

    @staticmethod
    def init_app(app):
        with open(app.config['AUTH_PRIVATE_KEY']) as f:
            app.config['AUTH_PRIVATE_KEY'] = f.read()

        with open(app.config['AUTH_PUBLIC_KEY']) as f:
            app.config['AUTH_PUBLIC_KEY'] = f.read()


class DevelopmentConfig(Config):
    DEBUG = True

    @staticmethod
    def init_app(app):
        Config.init_app(app)

        for hdler in app.logger.handlers:
            if isinstance(hdler, logging.FileHandler):
                if hdler.baseFilename == os.path.abspath(os.fspath(app.config['LOG_PATH'])):
                    return

        handler = RotatingFileHandler(app.config['LOG_PATH'],
                                      maxBytes=app.config['LOG_SIZE'],
                                      backupCount=app.config['LOG_COUNT'],
                                      encoding=app.config['LOG_ENCODING'])
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'
        )

        handler.setFormatter(formatter)
        handler.setLevel(logging.INFO)

        app.logger.addHandler(handler)


class ProductionConfig(Config):
    DEBUG = False

    @staticmethod
    def init_app(app):
        DevelopmentConfig.init_app(app)


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
