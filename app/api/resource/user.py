#!/usr/bin/env python
# encoding: utf-8

import uuid

from flask import request, abort, g
from flask_restful import Resource

from app import db
from app.models import User
from app.api.common.schema import UserRegisterSchema
from app.api.common.schema import UserSchema
from app.api.auth import authenticate

class UserController(Resource):

    @authenticate()
    def get(self, user_id):
        user = User.query.filter_by(user_id=user_id).first()
        if not user:
            abort(404, 'User {user_id} Not Found'.format(user_id=user_id))
        return { 'user': UserSchema().dump(user).data }

    @authenticate()
    def patch(self, user_id):
        if g.current_user.is_admin():
            user = User.query.filter_by(user_id=user_id).first()
            if not user:
                abort(404, 'User {user_id} Not Found'.format(user_id=user_id))
        elif g.current_user.user_id == user_id:
            user = g.current_user
        else:
            abort(403)

        schema = UserSchema()
        user_info, errors = schema.load(request.get_json())
        if errors:
            abort(400, errors)

        # ensure email unique
        if user_info.has_key('email') and \
           user_info['email'] != user.email and \
           User.query.filter_by(email=user_info['email']).first():
            abort(400, 'Email Already registered!')

        for key, value in user_info.iteritems():
            setattr(user, key, value)
        db.session.add(user)

        return { 'user': UserSchema().dump(user).data }

    @authenticate('admin')
    def delete(self, user_id):
        user = User.query.filter_by(user_id=user_id).first()
        if user:
            db.session.delete(user)
        return {}, 204


class UsersController(Resource):

    @authenticate('admin')
    def post(self):
        schema = UserRegisterSchema()
        user, errors = schema.load(request.get_json())
        if errors:
            abort(400, errors)

        user.user_id = uuid.uuid4().hex
        db.session.add(user)

        return { 'user': UserSchema().dump(user).data }, 201

    @authenticate()
    def get(self):
        users = User.query.all()
        schema = UserSchema(many=True)

        return { 'users': schema.dump(users).data }

