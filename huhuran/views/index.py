# coding: utf-8

from flask import url_for, redirect, Blueprint, g, render_template

bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    if g.user:
        return redirect(url_for('machine.index'))
    return render_template('init.html')

