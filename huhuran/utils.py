# coding: utf-8

from functools import wraps
from flask import g, url_for, redirect


def need_login(f):
    @wraps(f)
    def _(*args, **kwargs):
        if not g.user:
            return redirect(url_for('user.login'))
        return f(*args, **kwargs)
    return _

class Obj(object):pass

def get_user(info):
    if not info:
        return None
    u = Obj()
    u.id = info['id']
    u.name = info['name']
    u.email = info['email']
    u.admin = info['privilege']
    return u

