# coding: utf-8

from flask_restplus import fields
from .. import api


client_post_model = api.model('Client POST model', {
    'username': fields.String(required=True, min_length=3, max_length=32, description='Username'),
    'password': fields.String(required=True, min_length=3, max_length=16, description='Password'),
    'is_admin': fields.Boolean(required=False, default=False, description='Administrator status')
})

client_minimal_model = api.model('Client minimal model', {
    'id': fields.Integer(required=True, description='Unique ID'),
    'username': fields.String(required=True, description='Username'),
    'is_admin': fields.Boolean(default=False, description='Administrator status')
})

access_nested = api.model('Access nested', {
    'id': fields.Integer(required=True, description='Unique id'),
    'topic': fields.String(required=True, description='Topic'),
    'access': fields.Integer(required=True, description='Access type (1 for read only, 2 for read and write')
})

client_detail_model = api.inherit('Client detail model', client_minimal_model, {
    'accesses': fields.List(fields.Nested(access_nested), required=True, description='Access list')
})

client_container_model = api.model('Client container model', {
    'items': fields.List(fields.Nested(client_minimal_model), required=True, description='Client list')
})
