# Base Flask App

# Install and Run
    # pip install -r requirements.txt
    # python manager.py runserver

# Test
    >>> python manager.py shell
    >>> db.create_all()
    >>> import uuid
    >>> user = User(email=admin@example.com, role='admin', user_id=uuid.uuid4().hex)
    >>> user.password = '123456'
    >>> db.session.add(user)
    >>> db.session.commit()

    # get token for admin
    # http localhost:5000/v1/auth/tokens email=admin@example.com password=123456
    # create user
    # http localhost:5000/v1/users email=foo@bar password=123456 token:<token>
    # get user list
    # http localhost:5000/v1/users token:<token>
    # http localhost:5000/v1/users/<user_id> token:<token>
    # http PUT localhost:5000/v1/users/<user_id> email=bar@foo token:<token>
    # http DELETE localhost:5000/v1/users/<user_id> token:<token>

