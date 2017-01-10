#!/usr/bin/env python
# encoding: utf-8

from functools import wraps

from ..models import User
from flask import request, abort
from flask import g, make_response


def unauthorized():
    response = make_response()
    response.status_code = 401
    response.headers['WWW-Authenticate'] = 'xBasic realm="{0}"'.format('Authentication Required')
    return response

def verify_password(email_or_token, password):
    if password == '':
        g.current_user = User.verify_auth_token(email_or_token)
        g.token_used = True
        return g.current_user != None
    user = User.query.filter_by(email=email_or_token).first()
    if not user:
        return False
    g.current_user = user
    g.token_used = False
    return user.verify_password(password)

def authenticate(role=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = request.headers.get('token')
            if not token:
                abort(401)
            g.current_user = User.verify_auth_token(token)
            if role and not g.current_user.is_role(role):
                abort(403)
            return func(*args, **kwargs)
        return wrapper
    return decorator

