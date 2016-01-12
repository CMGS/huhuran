# coding: utf-8

from flask import (Blueprint, request, g, abort, jsonify,
                   render_template, url_for, redirect)
from eruhttp import EruException

from huhuran.ext import eru
from huhuran.config import PODNAME, DEPLOY_MODE
from huhuran.models import Machine, Image
from huhuran.utils import need_login

bp = Blueprint('machine', __name__, url_prefix='/machine')


@bp.route('/')
@need_login
def index():
    machines = Machine.get_by_user(g.user)
    return render_template('index.html', machines=machines)


@bp.route('/<machine_id>/update', methods=['GET', 'POST'])
def callback(machine_id):
    machine = Machine.get(machine_id)
    if not machine:
        return 'not found'

    data = request.get_json()
    container_id = data['container_id']
    status = data.get('status')
    machine.set_alive(status == 'start')
    if not machine.container_id:
        machine.set_container_id(container_id)
    return 'ok'


@bp.route('/create', methods=['GET', 'POST'])
@need_login
def create_machine():
    if request.method == 'GET':
        images = Image.list_all()
        return render_template('create_machine.html', images=images)

    name = request.form['name']
    image_name = request.form['image_name']
    if not (image_name and name):
        abort(400)

    image = Image.get_by_name(image_name)
    if not image:
        abort(400)

    machine = Machine.create(g.user, name)
    callback_url = url_for('machine.callback', machine_id=machine.id, _external=True)
    try:
        if DEPLOY_MODE == 'public':
            eru.deploy_public(PODNAME, image.appname, 1, image.version,
                              image.entrypoint, image.env, [image.network],
                              callback_url=callback_url)
        elif DEPLOY_MODE == 'private':
            eru.deploy_private(PODNAME, image.appname, 1, 1, image.version,
                              image.entrypoint, image.env, [image.network],
                              callback_url=callback_url)
    except EruException:
        pass
    return redirect(url_for('machine.index'))


@bp.route('/delete', methods=['POST'])
@need_login
def delete_machine():
    machine = Machine.get(request.form['machine_id'])
    if not machine:
        return jsonify(r=0)

    if machine.container_id:
        try:
            eru.remove_containers([machine.container_id])
        except EruException:
            pass

    machine.delete()
    return jsonify(r=0)


@bp.route('/create_image', methods=['GET', 'POST'])
@need_login
def create_image():
    if request.method == 'GET':
        images = Image.list_all()
        return render_template('create_image.html', images=images)

    name = request.form['name']
    addr = request.form['addr']
    desc = request.form['desc']
    appname = request.form['appname']
    version = request.form['version']
    entrypoint = request.form['entrypoint']
    env = request.form['env']
    network = request.form['network']
    Image.create(name, addr, appname, version, entrypoint, env, network, desc)
    return redirect(url_for('machine.create_image'))


@bp.errorhandler(403)
@bp.errorhandler(404)
def error_handler(e):
    return render_template('%s.html' % e.code), e.code
