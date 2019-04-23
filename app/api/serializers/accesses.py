# coding: utf-8

from flask_restplus import fields
from .. import api

access_post_model = api.model('Access post model', {
    'topic': fields.String(required=True, min_length=3, max_length=256, description='Topic'),
    'username': fields.String(required=True, min_length=3, max_length=32, desciption='Username'),
    'access': fields.Integer(required=True, min=1, max=2, default=1,
                             description='Access type (1 for read only, 2 for read and write')
})


access_patch_model = api.model('Access patch model', {
    'topic': fields.String(required=False, min_length=3, max_length=256, description='Totpic'),
    'access': fields.Integer(required=False, min=1, max=2, default=1,
                             description='Access type (1 for read only, 2 for read and write')
})

access_model = api.model('Access model', {
    'id': fields.Integer(required=True, description='Unique id'),
    'topic': fields.String(required=True, description='Topic'),
    'username': fields.String(required=True, desciption='Username'),
    'access': fields.Integer(required=True, description='Access type (1 for read only, 2 for read and write')
})

access_container_model = api.model('Access container model', {
    'items': fields.List(fields.Nested(access_model), required=True, description='Accesses list')
})
