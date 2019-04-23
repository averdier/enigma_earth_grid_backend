# coding: utf-8

from flask import Flask, request
from flask_cors import CORS
from config import config
from .extensions import db


def create_app(config_name='default'):
    from .api import blueprint as api_blueprint

    app = Flask(__name__)
    CORS(app, resources={
        r"/api/*": {"origins": "*"}
    })

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    app.register_blueprint(api_blueprint)

    extensions(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        if request.method == 'OPTIONS':
            response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
            headers = request.headers.get('Access-Control-Request-Headers')
            if headers:
                response.headers['Access-Control-Allow-Headers'] = headers

        return response

    return app


def extensions(flask_app):
    db.init_app(flask_app)

    with flask_app.app_context():
        from .models import User

        if User.query.first() is None:
            admin = User(
                username='rastadev',
                secret='rastadev'
            )
            db.session.add(admin)
            db.session.commit()
