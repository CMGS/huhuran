# coding: utf-8

from functools import wraps
from flask import g, url_for, redirect
from paramiko import SSHClient, AutoAddPolicy
from paramiko.ssh_exception import SSHException, AuthenticationException

from huhuran.config import DEFAULT_USER, DEFAULT_PASS


def need_login(f):
    @wraps(f)
    def _(*args, **kwargs):
        if not g.user:
            return redirect(url_for('user.login'))
        return f(*args, **kwargs)
    return _


def need_admin(f):
    @wraps(f)
    def _(*args, **kwargs):
        if not g.user or not int(g.user.admin):
            return redirect(url_for('machine.index'))
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
    u.pubkey = info.get('pubkey', '')
    return u


def add_pubkey(key, remote_addr):
    if not key:
        return False

    try:
        client = SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy())
        client.connect(remote_addr, username=DEFAULT_USER,
                       password=DEFAULT_PASS, timeout=5)
    except (SSHException, AuthenticationException):
        return False

    try:
        command = 'echo "%s" >> .ssh/authorized_keys' % key
        _, _, stderr = client.exec_command(command, timeout=5)
        return stderr.read() == ''
    finally:
        client.close()
