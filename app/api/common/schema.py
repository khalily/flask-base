#!/usr/bin/env python
# encoding: utf-8

from flask import abort
from marshmallow import Schema, fields, validate, validates, post_load
from marshmallow import ValidationError

from app.models import User


class UserRegisterSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True,
                          load_only=True,
                          validate=[validate.Length(min=6, max=16)])
    role = fields.Str(validate=[validate.OneOf(['admin', 'member'])])

    @validates('email')
    def validate_email(self, email):
        if User.query.filter_by(email=email).first():
            raise ValidationError('Eamil Already registered!')

    @post_load
    def make_user(self, data):
        user = User(email=data['email'])
        user.password = data['password']
        return user


class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True,
                          load_only=True,
                          validate=[validate.Length(min=6, max=16)])

    @post_load
    def make_user(self, data):
        user = User.query.filter_by(email=data['email']).first()
        if not user:
            abort(401, 'Invalid Username')
        if not user.verify_password(data['password']):
            abort(401, 'Invalid Password')
        return user


class UserSchema(Schema):
    id = fields.Str(dump_only=True, attribute='user_id')
    email = fields.Email()
    password = fields.Str(load_only=True,
                          validate=[validate.Length(min=6, max=16)])
    role = fields.Str(dump_only=True)

