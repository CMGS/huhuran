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
