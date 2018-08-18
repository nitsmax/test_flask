import os
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import Blueprint, request, Response
from flask import current_app as app
from app.commons import build_response
from app.users.models import User
from app.users.tasks import save_user, transpose_user, create_jwttoken
from app.commons.utils import update_document
from werkzeug.security import generate_password_hash, check_password_hash


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

    return build_response.build_json({'email': email, 'auth_token': create_jwttoken(email)[1].decode('utf-8')})

@auth.route('/signup', methods=['POST'])
def signup():
    """
    SignUp to user and return a token
    """
    content = request.get_json(silent=True)

    email = content.get("email")

    user = User.objects(email=email).first()
    
    '''
    If user exit Update it with latest info
    '''
    if not user:
        user = User()

    try:
        save_response = save_user(user)
        if 'error' in save_response:
            raise Exception(save_response['error'])
        else:
            return build_response.build_json({'email': email, 'auth_token': create_jwttoken(email)[1].decode('utf-8')})
    except Exception as e:
        return build_response.build_json({"error": str(e)})
