# coding: utf-8

import datetime
import sqlalchemy.exc
from sqlalchemy.ext.declarative import declared_attr
from eruhttp import EruException

from huhuran.ext import db, rds, eru

_ERU_SSH_ROUTE_KEY = 'mimiron:%s:route'


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
    is_alive = db.Column(db.Boolean, default=False)

    @classmethod
    def create(cls, user, name):
        try:
            r = cls(name=name, user_id=user.id)
            db.session.add(r)
            db.session.commit()
            return r
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()
            return None

    @classmethod
    def get_by_user(cls, user):
        return cls.query.filter_by(user_id=user.id).all()

    @property
    def user(self):
        return User.get(self.user_id)

    def set_container_id(self, container_id):
        try:
            container = eru.get_container(container_id)
            backend = container['backends'][0]
            rds.hset(_ERU_SSH_ROUTE_KEY % self.user.name, self.name, backend)
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
        rds.hdel(_ERU_SSH_ROUTE_KEY % self.user.name, self.name)
        db.session.delete(self)
        db.session.commit()


class User(Base):
    __tablename__ = 'user'
    name = db.Column(db.String(255), index=True, nullable=False, default='')
    email = db.Column(db.String(255), unique=True, nullable=False, default='')
    admin = db.Column(db.Boolean)

    @classmethod
    def get_or_create(cls, name, email):
        u = cls.get_by_email(email)
        if u:
            return u
        try:
            u = cls(name=name, email=email, admin=False)
            db.session.add(u)
            db.session.commit()
            return u
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()
            return None

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter(cls.email == email).first()

    @classmethod
    def get_by_name(cls, name):
        return cls.query.filter(cls.name == name).first()


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
