# coding: utf-8

from flask.ext.sqlalchemy import SQLAlchemy
from eruhttp import EruClient
from huhuran.config import ERU_URL

db = SQLAlchemy()
eru = EruClient(ERU_URL)
