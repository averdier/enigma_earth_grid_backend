# coding: utf-8

from flask_restplus import fields
from .. import api

chunk_post_model = api.model('Chunk POST model', {
    'name': fields.String(required=True, min_length=3, max_length=32, description='Name'),
    'long': fields.Float(required=True, description='Longitude'),
    'topic': fields.String(required=True, description='Topic string'),
    'lat': fields.Float(required=True, description='Latitude'),
    'price': fields.Float(required=True, description='Price'),
    'description': fields.String(required=False, description='Description')
})

chunk_search_model = api.model('Chunk POST search model', {
    'long': fields.Float(required=True, description='Longitude'),
    'lat': fields.Float(required=True, description='Latitude'),
    'size': fields.Float(required=False, default=1)
})

chunk_model = api.model('Chunk model', {
    'id': fields.Integer(required=True, description='Chunk unique ID'),
    'name': fields.String(required=True, min_length=3, max_length=32, description='Name'),
    'long': fields.Float(required=True, description='Longitude'),
    'lat': fields.Float(required=True, description='Latitude'),
    'price': fields.Float(required=True, description='Price'),
    'topic': fields.String(required=True, description='Topic'),
    'description': fields.String(required=False, description='Description'),
    'created_at': fields.DateTime(required=True, description='Created_at'),
})

chunk_res_search_model = api.inherit('Chunk response search model', chunk_model, {
    'owned': fields.Boolean(required=True)
})

chunk_container_model = api.model('Chunk container model', {
    'items': fields.List(fields.Nested(chunk_model), required=True, description='Chunk list')
})

chunk_res_search_container_model = api.model('Chunk response search container model', {
    'items': fields.List(fields.Nested(chunk_res_search_model), required=True, description='Chunk list')
})
