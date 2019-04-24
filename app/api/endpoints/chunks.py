# coding: utf-8

from flask import request, g
from flask_restplus import Namespace, Resource, abort
from .. import auth
from ..serializers.chunks import chunk_container_model, chunk_model, chunk_post_model, chunk_search_model, chunk_res_search_container_model
from app.extensions import db
from app.models import Chunk, User

ns = Namespace('chunks', description='Chunks related operations')


@ns.route('/')
class ChunkCollection(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(chunk_container_model)
    def get(self):
        """
        Return chunks list
        """
        if g.client.is_admin:
            return {'items': Chunk.query.all()}

        return {'items': g.client.chunks.all()}

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
            long=data['long'],
            topic=data['topic'],
            price=data['price']
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
    decorators = [auth.login_required]

    @ns.doc(response={
        409: 'Value exist',
        400: 'Validation error'
    })
    @ns.expect(chunk_search_model)
    @ns.marshal_with(chunk_res_search_container_model)
    def post(self):
        """
        Search chunk by geo
        """
        data = request.json
        client_chunks = g.client.chunks.all()
        chunks = Chunk.query.filter(data['lat'] - data['size'] <= Chunk.lat, Chunk.lat <= data['lat'] + data['size']).filter(data['long'] - data['size'] <= Chunk.long, Chunk.long <= data['long'] + data['size']).all()

        for chunk in chunks:
            chunk.owned = chunk in client_chunks

        return {'items': chunks}
