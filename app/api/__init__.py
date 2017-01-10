#!/usr/bin/env python
# encoding: utf-8

from flask import Blueprint
from flask_restful import Api

api_bp = Blueprint('api', __name__)

api = Api(api_bp)


from resource import UsersController, UserController
from resource import TokenController

api.add_resource(UsersController, '/users')
api.add_resource(UserController, '/users/<string:user_id>')
api.add_resource(TokenController, '/auth/tokens')

from . import errors
