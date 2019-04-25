# coding: utf-8

from flask_restplus import fields
from .. import api
from .chunks import chunk_model


user_post_model = api.model('User POST model', {
    'username': fields.String(required=True, min_length=3, max_length=32, description='Username'),
    'secret': fields.String(required=True, min_length=3, max_length=16, description='Secret'),
    'email': fields.String(required=True, description='Email'),
    'last_name': fields.String(required=True, description='Last Name'),
    'first_name': fields.String(required=True, description='First Name'),
    'deposit': fields.Float(required=False, default=0, description='Deposit'),
    'is_admin': fields.Boolean(required=False, default=False, description='Is Admin'),
})

user_model = api.model('User model', {
    'id': fields.Integer(required=True, description='User unique ID'),
    'username': fields.String(required=True, min_length=3, max_length=32, description='Username'),
    'email': fields.String(required=True, description='Email'),
    'last_name': fields.String(required=True, description='Last Name'),
    'first_name': fields.String(required=True, description='First Name'),
    'deposit': fields.Float(required=True, description='Deposit'),
    'is_admin': fields.Boolean(required=True, description='Is_admin'),
    'created_at': fields.DateTime(required=True, description='Created_at'),
})

user_detail_model = api.inherit('User detail model', user_model, {
    'chunks': fields.List(fields.Nested(chunk_model))
})

user_container_model = api.model('User container model', {
    'items': fields.List(fields.Nested(user_model), required=True, description='User list')
})

user_chunk_model = api.model('User chunk model', {
    'chunk_id': fields.Integer(required=True, description="Chunk Id")
})

user_deposit_model = api.model('User deposit model', {
    'amount': fields.Float(required=True, description='Amount to deposit', min=0)
})
