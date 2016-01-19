#!/usr/bin/python
#coding:utf-8

from flask import Blueprint, g, render_template

from huhuran.models import Machine
from huhuran.utils import need_admin

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/')
@need_admin
def index():
    machines, total = Machine.list_machines(start=g.start, limit=g.limit)
    return render_template('admin.html',
        machines=machines, total=total, endpoint='admin.index',
    )

