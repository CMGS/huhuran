# coding: utf-8

import datetime
import sqlalchemy.exc
from sqlalchemy.ext.declarative import declared_attr
from eruhttp import EruException

from huhuran.ext import db, eru


class Base(db.Model):

    __abstract__ = True

    @declared_attr
    def id(cls):
        return db.Column('id', db.Integer, primary_key=True, autoincrement=True)

    @classmethod
    def get(cls, id):
        return cls.query.filter(cls.id == id).first()

    @classmethod
    def get_multi(cls, ids):
        return [cls.get(i) for i in ids]


class Machine(Base):
    __tablename__ = 'machine'
    name = db.Column(db.String(255), nullable=False, default='')
    container_id = db.Column(db.String(64), nullable=False, default='')
    time = db.Column(db.DateTime, default=datetime.datetime.now)
    user_id = db.Column(db.Integer, index=True)
    user_name = db.Column(db.String(255), index=True)
    netaddr = db.Column(db.String(16), index=True)
    is_alive = db.Column(db.Boolean, default=False)

    @classmethod
    def create(cls, user, name):
        try:
            r = cls(name=name, user_id=user.id, user_name=user.name)
            db.session.add(r)
            db.session.commit()
            return r
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()
            return None

    @classmethod
    def get_by_user(cls, user):
        return cls.query.filter_by(user_id=user.id).all()

    @classmethod
    def list_machines(cls, start=0, limit=20):
        q = cls.query.order_by(cls.id.desc())
        total = q.count()
        q = q.offset(start)
        if limit is not None:
            q = q.limit(limit)
        return q.all(), total

    def set_netaddr(self, netaddr):
        self.netaddr = netaddr
        db.session.add(self)
        db.session.commit()

    def set_container_id(self, container_id):
        try:
            eru.get_container(container_id)
        except (EruException, KeyError):
            return

        self.container_id = container_id
        db.session.add(self)
        db.session.commit()

    def set_alive(self, alive):
        self.is_alive = alive
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Image(Base):
    __tablename__ = 'image'
    name = db.Column(db.String(255), unique=True, nullable=False)
    addr = db.Column(db.String(255))
    desc = db.Column(db.Text)
    appname = db.Column(db.String(255))
    version = db.Column(db.String(255))
    entrypoint = db.Column(db.String(255))
    env = db.Column(db.String(255))
    network = db.Column(db.String(255))

    @classmethod
    def create(cls, name, addr, appname, version, entrypoint, env, network, desc=''):
        try:
            c = cls(name=name, addr=addr, appname=appname, version=version,
                    entrypoint=entrypoint, env=env, network=network, desc=desc)
            db.session.add(c)
            db.session.commit()
            return c
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()
            return None

    @classmethod
    def get_by_name(cls, name):
        return cls.query.filter(cls.name == name).first()

    @classmethod
    def list_all(cls, start=0, limit=20):
        q = cls.query.order_by(cls.id.desc())
        return q[start:start+limit]

    def delete(self):
        db.session.delete(self)
        db.session.commit()
