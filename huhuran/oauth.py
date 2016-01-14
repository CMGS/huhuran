#!/usr/bin/python
#coding:utf-8

from flask import current_app
from flask_oauthlib.client import OAuth
from huhuran import config

oauth = OAuth(current_app)
sso = oauth.remote_app(
    'sso',
    consumer_key=config.OAUTH2_CLIENT_ID,
    consumer_secret=config.OAUTH2_CLIENT_SECRET,
    request_token_params={'scope': 'email'},
    base_url=config.OAUTH2_BASE_URL,
    request_token_url=None,
    access_token_url=config.OAUTH2_ACCESS_TOKEN_URL,
    authorize_url=config.OAUTH2_AUTHORIZE_URL,
)

