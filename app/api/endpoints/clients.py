# coding: utf-8

from flask import request
from flask_restplus import Namespace, Resource, abort
from .. import auth
from ..serializers.clients import client_container_model, client_minimal_model, client_post_model, client_detail_model
from app.extensions import db
from app.models import MqttClient

ns = Namespace('clients', description='Clients related operations')


@ns.route('/')
class ClientCollection(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(client_container_model)
    def get(self):
        """
        Return mqtt clients list
        """

        return {'items': MqttClient.query.all()}

    @ns.marshal_with(client_minimal_model, code=201, description='Client successfully added.')
    @ns.doc(response={
        400: 'Validation error'
    })
    @ns.expect(client_post_model)
    def post(self):
        """
        Add mqtt client
        """
        data = request.json

        if MqttClient.query.filter_by(username=data['username']).first() is not None:
            abort(400, error='Username already exist')

        client = MqttClient()
        client.username = data['username']
        client.hash_password(data['password'])
        client.is_admin = data['is_admin']

        db.session.add(client)
        db.session.commit()

        return client, 201


@ns.route('/<int:client_id>')
@ns.response(404, 'Client not found')
class ClientItem(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(client_detail_model)
    def get(self, client_id):
        """
        Get client
        """
        client = MqttClient.query.get_or_404(client_id)

        return client

    @ns.response(204, 'Client successfully deleted.')
    def delete(self, client_id):
        """
        Delete client
        """

        client = MqttClient.query.get_or_404(client_id)

        db.session.delete(client)
        db.session.commit()

        return 'Client successfully deleted.', 204
