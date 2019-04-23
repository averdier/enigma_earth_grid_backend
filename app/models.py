# coding: utf-8

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from plugins.hashing_passwords import make_hash


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    username = db.Column(db.String(32), index=True, unique=True)
    secret_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False, unique=True)
    last_name = db.Column(db.String(32))
    first_name = db.Column(db.String(32))
    deposit = db.Column(db.Float(), default=0)
    is_admin = db.Column(db.Boolean(), nullable=False, default=False)

    @property
    def secret(self):
        return self.secret_hash

    @secret.setter
    def secret(self, pwd):
        self.secret_hash = generate_password_hash(pwd)

    def check_secret(self, pwd):
        return check_password_hash(self.secret_hash, pwd)


class Chunk(db.Model):
    __tablename__ = "chunks"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    topic = db.Column(db.String(32), nullable=False)
    name = db.Column(db.String(32), nullable=False)
    long = db.Column(db.Float(), nullable=False)
    lat = db.Column(db.Float(), nullable=False)


class MqttClient(db.Model):
    __tablename__ = 'mqtt_clients'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    username = db.Column(db.String(32), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean(), nullable=False, default=False)
    accesses = db.relationship('MqttAccess', lazy='dynamic',
                               backref=db.backref('client', lazy=True))

    def hash_password(self, password):
        """
        Set new client password

        :param password:
        :return:
        """
        self.password = make_hash(password)


class MqttAccess(db.Model):
    __tablename__ = 'mqtt_access'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    topic = db.Column(db.String(256), nullable=False)
    access = db.Column(db.Integer, nullable=False, default=1)
    username = db.Column(db.String(32), db.ForeignKey('mqtt_clients.username'))
