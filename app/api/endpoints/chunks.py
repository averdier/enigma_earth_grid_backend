# coding: utf-8

from flask import request
from flask_restplus import Namespace, Resource, abort
from .. import auth
from ..serializers.chunks import chunk_container_model, chunk_model, chunk_post_model, chunk_search_model
from app.extensions import db
from app.models import Chunk

ns = Namespace('chunks', description='Chunks related operations')


@ns.route('/')
class ChunkCollection(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(chunk_container_model)
    def get(self):
        """
        Return chunks list
        """

        return {'items': Chunk.query.all()}

    @ns.marshal_with(chunk_model, code=201, description='Chunk successfully added.')
    @ns.doc(response={
        409: 'Value exist',
        400: 'Validation error'
    })
    @ns.expect(chunk_post_model)
    def post(self):
        """
        Add chunk
        """

        data = request.json

        if Chunk.query.filter_by(name=data['name']).first() is not None:
            abort(409, error='Name already exist')

        chunk = Chunk(
            name=data['name'],
            lat=data['lat'],
            long=data['long']
        )

        db.session.add(chunk)
        db.session.commit()

        return chunk, 201


@ns.route('/<int:chunk_id>')
@ns.response(404, 'Chunk not found')
class ChunkItem(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(chunk_model)
    def get(self, chunk_id):
        """
        Get chunk
        """

        chunk = Chunk.query.get_or_404(chunk_id)

        return chunk

    @ns.response(204, 'Chunk successfully deleted.')
    def delete(self, chunk_id):
        """
        Delete chunk
        """
        chunk = Chunk.query.get_or_404(chunk_id)

        db.session.delete(chunk)
        db.session.commit()

        return 'Chunk successfully deleted.', 204


@ns.route('/search')
class ChunkSearch(Resource):
    @ns.doc(response={
        409: 'Value exist',
        400: 'Validation error'
    })
    @ns.expect(chunk_search_model)
    def post(self):
        """
        Search chunk by geo
        """

        data = request.json
        chunks = Chunk.query.filter(data['lat'] - 0.25 <= Chunk.lat <= data['lat'] + 0.25 and data['long'] - 0.25 <= Chunk.long <= data['long'] + 0.25).all()

        return {'items': chunks}
