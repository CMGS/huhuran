# coding: utf-8

import os

DEBUG = bool(os.getenv('DEBUG', ''))

MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
MYSQL_PORT = int(os.getenv('MYSQL_PORT', '3306'))
MYSQL_USER = os.getenv('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'huhuran')

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', '6379'))

SQLALCHEMY_POOL_SIZE = 100
SQLALCHEMY_POOL_TIMEOUT = 10
SQLALCHEMY_POOL_RECYCLE = 2000

SERVER_PORT = int(os.getenv('SERVER_PORT', '5000'))
SERVER_NAME = os.getenv('SERVER_NAME', '') or None
SECRET_KEY = os.getenv('SECRET_KEY', '')

OPENID_LOGIN_URL = os.getenv('OPENID_LOGIN_URL', 'http://openids-web.intra.hunantv.com/oauth/login?return_to=%s&url=%s&days=14')
OPENID_PROFILE_URL = os.getenv('OPENID_PROFILE_URL', 'http://openids-web.intra.hunantv.com/oauth/profile/')

ERU_URL = os.getenv('ERU_URL', '')
DEPLOY_MODE = os.getenv('DEPLOY_MODE', 'public')
PODNAME = os.getenv('PODNAME', 'dev')
GROUPNAME = os.getenv('GROUPNAME', 'group')

try:
    from .local_config import *
except ImportError:
    pass

SQLALCHEMY_DATABASE_URI = 'mysql://{0}:{1}@{2}:{3}/{4}'.format(
    MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE,
)
