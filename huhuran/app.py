# coding: utf-8

import logging

from flask import Flask, request, g, session
from werkzeug.utils import import_string

from huhuran.ext import db
from huhuran.oauth import sso
from huhuran.utils import get_user
from huhuran.utils import paginator_kwargs

blueprints = (
    'admin',
    'index',
    'user',
    'machine',
)

def create_app():
    app = Flask(__name__, static_url_path='/huhuran/static')
    app.config.from_object('huhuran.config')
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', True)
    app.secret_key = app.config['SECRET_KEY']

    logging.basicConfig(format='%(levelname)s:%(asctime)s:%(message)s',
                        level=logging.INFO)

    for ext in (db, ):
        ext.init_app(app)

    for bp in blueprints:
        import_name = '%s.views.%s:bp' % (__package__, bp)
        app.register_blueprint(import_string(import_name))

    for fl in (max, min, paginator_kwargs):
        app.add_template_global(fl)

    @app.before_request
    def init_global_vars():
        g.user = 'sso' in session and get_user(sso.get('me').data) or None
        g.start = request.args.get('start', type=int, default=0)
        g.limit = request.args.get('limit', type=int, default=20)

    return app
