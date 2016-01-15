# coding: utf-8

import os

DEBUG = bool(os.getenv('DEBUG', ''))

MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
MYSQL_PORT = int(os.getenv('MYSQL_PORT', '3306'))
MYSQL_USER = os.getenv('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'huhuran')

SQLALCHEMY_POOL_SIZE = 100
SQLALCHEMY_POOL_TIMEOUT = 10
SQLALCHEMY_POOL_RECYCLE = 2000

SERVER_PORT = int(os.getenv('SERVER_PORT', '5000'))
SERVER_NAME = os.getenv('SERVER_NAME', '') or None
SECRET_KEY = os.getenv('SECRET_KEY', 'wolegeca69ooxx')

OAUTH2_CLIENT_ID = os.getenv('OAUTH2_CLIENT_ID', '')
OAUTH2_CLIENT_SECRET = os.getenv('OAUTH2_CLIENT_SECRET', '')
OAUTH2_ACCESS_TOKEN_URL = os.getenv('OAUTH2_ACCESS_TOKEN_URL', '')
OAUTH2_AUTHORIZE_URL = os.getenv('OAUTH2_AUTHORIZE_URL', '')
OAUTH2_BASE_URL = os.getenv('OAUTH2_BASE_URL', '')

ERU_URL = os.getenv('ERU_URL', '')
PODNAME = os.getenv('PODNAME', 'dev')
DEFAULT_PASS = os.getenv('DEFAULT_PASS', '')
DEFAULT_USER = os.getenv('DEFAULT_USER', '')
DEPLOY_MODE = os.getenv('DEPLOY_MODE', 'public')

try:
    from .local_config import *
except ImportError:
    pass

SQLALCHEMY_DATABASE_URI = 'mysql://{0}:{1}@{2}:{3}/{4}'.format(
    MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE,
)
