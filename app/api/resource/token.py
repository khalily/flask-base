#!/usr/bin/env python
# encoding: utf-8

import datetime

from flask import request, abort
from flask_restful import Resource

from app.api.common.schema import UserLoginSchema


class TokenController(Resource):

    def post(self):
        schem = UserLoginSchema()
        user, errors = schem.load(request.get_json())
        if errors:
            abort(400, errors)

        token = user.generate_auth_token()
        expired_in = datetime.datetime.utcnow() + \
                     datetime.timedelta(seconds=3600)
        return {
            'token': {
                'id': token,
                'expired_in': expired_in.isoformat()
            }
        }
