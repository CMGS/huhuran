# coding: utf-8

from flask import Blueprint, request, session, redirect, url_for, abort

from huhuran.utils import need_login
from huhuran.oauth import sso

bp = Blueprint('user', __name__, url_prefix='/user')

@sso.tokengetter
def get_oauth_token():
    return session.get('sso')

@bp.route('/authorized')
def authorized():
    resp = sso.authorized_response()
    if resp is None:
        abort(400)
    session['sso'] = (resp['access_token'], '')
    return redirect(url_for('user.login'))

@bp.route('/login/')
def login():
    if 'sso' in session:
        return redirect(url_for('index.index'))
    return sso.authorize(
        callback=url_for('user.authorized', _external=True)
    )

@bp.route('/logout/')
@need_login
def logout():
    session.pop('sso')
    return redirect(url_for('index.index'))

