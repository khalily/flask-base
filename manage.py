#!/usr/bin/env python
# encoding: utf-8

import os
from app import create_app, db
from app.models import User

from flask_script import Manager


app = create_app(os.getenv('FLASK_CONFIG') or 'devlopment')

manager = Manager(app)

@manager.shell
def make_context():
    return dict(app=app, db=db, User=User)

if __name__ == '__main__':
    manager.run()
