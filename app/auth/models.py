from flask import current_app as app
from app.users.models import User
from app.commons import build_response
from flask import request, g
import functools
import jwt


def login_required(f):
    @functools.wraps(f)
    def wrap(*args, **kwargs):
        header = request.headers.get('Authorization')
        try:
            _, token = header.split()
        except Exception as e:
            return build_response.build_json({"error": str(e)})

        try:
            decoded = jwt.decode(token, app.config['KEY'], algorithms='HS256')
        except jwt.DecodeError:
            return build_response.build_json({"error": 'Token is not valid.'})
        except jwt.ExpiredSignatureError:
            return build_response.build_json({"error": 'Token is expired.'})
        email = decoded['email']
        user = User.objects(email=email).first()
        if not user:
            return build_response.build_json({"error": 'User is not found.'})

        g.user = user
        return f(*args, **kwargs)
    return wrap

