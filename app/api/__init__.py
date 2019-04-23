# -*- coding: utf-8 -*-

import jwt
from flask import Blueprint, current_app, g
from flask_restplus import Api
from flask_httpauth import HTTPTokenAuth
from app.models import User

blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint,
          title='Earth grid API',
          version='0.1',
          description='Python micro service for earth grid system',
          doc='/',
          authorizations={
              'tokenKey': {
                  'type': 'apiKey',
                  'in': 'header',
                  'name': 'Authorization'
              }
          },
          security='tokenKey'
          )

auth = HTTPTokenAuth(scheme='Bearer')


@auth.verify_token
def verify_token(token):
    try:
        response = jwt.decode(
            token,
            current_app.config['AUTH_PUBLIC_KEY'],
            audience=current_app.config['AUTH_AUDIENCE']
        )
        u = User.query.get(int(response['user']['id']))

        if u:
            g.client = u
            g.client_token = token
            return True

        return False

    except Exception as ex:
        current_app.logger.warning('Unable to verify token [{0}], reason : {1}'.format(
            token, ex
        ))

        return False


from .endpoints.clients import ns as client_namespace
from .endpoints.users import ns as users_namespace
from .endpoints.accesses import ns as accesses_namespace
from .endpoints.auth import ns as auth_namespace
from .endpoints.chunks import ns as chunks_namespace

api.add_namespace(auth_namespace)
api.add_namespace(client_namespace)
api.add_namespace(users_namespace)
api.add_namespace(accesses_namespace)
api.add_namespace(chunks_namespace)
