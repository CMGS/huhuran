# coding: utf-8

import sys
import os
sys.path.append(os.path.abspath('.'))

from huhuran.app import create_app
from huhuran.ext import db
from huhuran.models import Machine, Image

def flushdb(app):
    with app.app_context():
        db.drop_all()
        db.create_all()

if __name__ == '__main__':
    app = create_app()
    if app.config['MYSQL_HOST'] in ('127.0.0.1', 'localhost') or '--force' in sys.argv:
        flushdb(app)
    else:
        print 'you are not doing this on your own computer,'
        print 'if sure, add --force to flush database.'
