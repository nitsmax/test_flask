import os
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import Blueprint, request, Response
from flask import current_app as app
from app.commons import build_response
from app.users.models import User
from app.commons.utils import update_document
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import jwt


auth = Blueprint('auth_blueprint', __name__,
                    url_prefix='/api/auth')


@auth.route('/login', methods=['POST'])
def login():
    """
    Login to user and return a token
    """

    content = request.get_json(silent=True)

    email = content.get("email")
    password = content.get("password")

    user = User.objects(email=email).first()
    
    if not user:
        return build_response.build_json({"error": 'User is not found.'})
    
    if not check_password_hash(user.password, password):
        return build_response.build_json({"error": 'Password is incorrect.'})

    exp = datetime.datetime.utcnow() + datetime.timedelta(hours=app.config['TOKEN_EXPIRE_HOURS'])
    auth_token = jwt.encode({'email': email, 'exp': exp},
                         app.config['KEY'], algorithm='HS256')

    refresh_token = jwt.encode({'email': email},
                         app.config['KEY'], algorithm='HS256')

    return build_response.build_json({'email': email, 'auth_token': auth_token.decode('utf-8'), 'refresh_token': refresh_token.decode('utf-8')})

@auth.route('/signup', methods=['POST'])
def signup():
    """
    SignUp to user and return a token
    """
    user = User()

    content = request.get_json(silent=True)

    email = content.get("email")

    user = User.objects(email=email).first()
    
    '''
    If user exit Update it with latest info
    '''
    if user:
        return build_response.build_json({"error": 'User is not found.'})
    else:
        

    