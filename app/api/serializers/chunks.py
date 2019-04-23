# coding: utf-8

from flask_restplus import fields
from .. import api

chunk_post_model = api.model('Chunk POST model', {
    'name': fields.String(required=True, min_length=3, max_length=32, description='Name'),
    'long': fields.Float(required=True, description='Longitude'),
    'lat': fields.Float(required=True, description='Latitude')
})

chunk_search_model = api.model('Chunk POST search model', {
    'long': fields.Float(required=True, description='Longitude'),
    'lat': fields.Float(required=True, description='Latitude')
})

chunk_model = api.model('Chunk model', {
    'id': fields.Integer(required=True, description='Chunk unique ID'),
    'name': fields.String(required=True, min_length=3, max_length=32, description='Name'),
    'long': fields.Float(required=True, description='Longitude'),
    'lat': fields.Float(required=True, description='Latitude'),
    'created_at': fields.DateTime(required=True, description='Created_at')
})

chunk_container_model = api.model('Chunk container model', {
    'items': fields.List(fields.Nested(chunk_model), required=True, description='Chunk list')
})
