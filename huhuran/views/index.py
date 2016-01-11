# coding: utf-8

from flask import url_for, redirect, Blueprint

bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    return redirect(url_for('machine.index'))
