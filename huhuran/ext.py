# coding: utf-8

from flask.ext.sqlalchemy import SQLAlchemy
from eruhttp import EruClient
from redis import Redis
from huhuran.config import ERU_URL, REDIS_HOST, REDIS_PORT

db = SQLAlchemy()
eru = EruClient(ERU_URL)
rds = Redis(REDIS_HOST, REDIS_PORT)
