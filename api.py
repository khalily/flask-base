#!/usr/bin/env python
# encoding: utf-8

from flask import Flask, request
from flask_restful import Resource, Api

from marshmallow import Schema, fields, validates, ValidationError


app = Flask(__name__)
api = Api(app)

class RealServerSchema(Schema):
    id = fields.Str()
    ip = fields.Str()
    port = fields.Int()
    weight = fields.Int()

class ServiceSchema(Schema):
    id = fields.Str()
    vip = fields.Str()
    port = fields.Int()
    sched = fields.Str()
    fwd = fields.Str()
    real_servers = fields.Nested(RealServerSchema, many=True)

    @validates('port')
    def validate_port(self, port):
        if not 0 < port < 65535 + 1:
            raise ValidationError('port must be > 0 and < 65536')

class Service(Resource):
    def get(self, service_id):
        pass

    def put(self):
        pass

    def delete(self):
        pass

class Services(Resource):
    def get(self):
        rss = [
            {
                'ip': '192.168.2.2',
                'port': 8000,
                'weight': 10
            },
        ]

        service = {
            'vip': '192.168.1.1',
            'port': 8000,
            'sched': 'wrr',
            'fwd': 'DR',
            'real_servers': [rs for rs in rss]
        }
        return [service]

    def post(self):
        data = request.form['data']
        return {'data': data}

class Index(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(Index, '/')
api.add_resource(Services, '/services')
api.add_resource(Service, '/services/<string:service_id>')

if __name__ == '__main__':
    app.run(debug=True)

