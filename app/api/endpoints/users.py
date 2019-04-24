# coding: utf-8

from flask import request, g
from flask_restplus import Namespace, Resource, abort
from .. import auth
from ..serializers.users import user_container_model, user_model, user_post_model, user_chunk_model, user_detail_model, user_deposit_model
from ..serializers.chunks import chunk_model
from app.extensions import db
from app.models import User, Chunk

ns = Namespace('users', description='Users related operations')


@ns.route('/')
class UserCollection(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(user_container_model)
    def get(self):
        """
        Return users list
        """

        return {'items': User.query.all()}

    @ns.marshal_with(user_model, code=201, description='User successfully added.')
    @ns.doc(response={
        409: 'Value exist',
        400: 'Validation error'
    })
    @ns.expect(user_post_model)
    def post(self):
        """
        Add user
        """

        data = request.json

        if User.query.filter_by(username=data['username']).first() is not None:
            abort(409, error='Username already exist')
        if User.query.filter_by(email=data['email']).first() is not None:
            abort(409, error='Email already exist')

        user = User(
            username=data['username'],
            secret=data['secret'],
            email=data['email'],
            last_name=data['last_name'],
            first_name=data['first_name'],
            deposit=data['deposit'],
            is_admin=data['is_admin'],
        )

        db.session.add(user)
        db.session.commit()

        return user, 201


@ns.route('/<int:user_id>')
@ns.response(404, 'User not found')
class UserItem(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(user_detail_model)
    def get(self, user_id):
        """
        Get user
        """

        user = User.query.get_or_404(user_id)

        return user

    @ns.response(204, 'User successfully deleted.')
    def delete(self, user_id):
        """
        Delete user
        """
        user = User.query.get_or_404(user_id)

        db.session.delete(user)
        db.session.commit()

        return 'User successfully deleted.', 204


@ns.route('/chunks')
@ns.response(404, 'Chunk not found')
class ChunkUserItem(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(user_detail_model, code=201, description='Chunk successfully added to user.')
    @ns.doc(response={
        409: 'Value exist',
        400: 'Validation error'
    })
    @ns.expect(user_chunk_model)
    def post(self):
        """
        Add chunk to current user
        """

        data = request.json
        chunk = Chunk.query.get_or_404(data['chunk_id'])

        if g.client.deposit - chunk.price < 0:
            abort(400, error='User have not enough money')
        if g.client.have_chunk(chunk) is True:
            abort(400, error='User already have this chunk')

        g.client.deposit -= chunk.price
        g.client.chunks.append(chunk)

        db.session.add(g.client)
        db.session.commit()

        return g.client, 201


@ns.route('/deposit')
@ns.response(404, 'User not found')
class ChunkUserItem(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(user_model, code=201, description='Chunk successfully added to user.')
    @ns.doc(response={
        409: 'Value exist',
        400: 'Validation error'
    })
    @ns.expect(user_deposit_model)
    def post(self):
        """
        Deposit money
        """

        data = request.json
        g.client.deposit += data['amount']

        db.session.add(g.client)
        db.session.commit()

        return g.client, 201
