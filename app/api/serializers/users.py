# coding: utf-8

from flask_restplus import fields
from .. import api


user_post_model = api.model('User POST model', {
    'username': fields.String(required=True, min_length=3, max_length=32, description='Username'),
    'secret': fields.String(required=True, min_length=3, max_length=16, description='Secret')
})

user_model = api.model('User model', {
    'id': fields.Integer(required=True, description='User unique ID'),
    'username': fields.String(required=True, min_length=3, max_length=32, description='Username'),
    'is_admin': fields.Boolean(required=True, default=False),
    'created_at': fields.DateTime(required=True, description='Created_at')
})

user_container_model = api.model('User container model', {
    'items': fields.List(fields.Nested(user_model), required=True, description='User list')
})
