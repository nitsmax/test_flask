import os
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import Blueprint, request, Response, g
from flask import current_app as app
from app.commons import build_response
from app.users.models import User
from app.auth.models import login_required, admin_required
from app.users.tasks import save_user, transpose_user, create_jwttoken,getUserBySoicalId
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
        return build_response.build_json({"status":False, "error": 'User is not found.'})
    
    if not check_password_hash(user.password, password):
        return build_response.build_json({"status":False, "error": 'Password is incorrect.'})

    return build_response.build_json(
        {
            'status':True,
            'membership': 'Free' if user.membershipPlan == 0 else 'Paid',
            'auth_token': create_jwttoken(1,user.email)[1].decode('utf-8')
        }
    )
    return build_response.build_json({'status':True, 'auth_token': create_jwttoken(1,email)[1].decode('utf-8')})

@auth.route('/signup', methods=['POST'])
def signup():
    """
    SignUp to user and return a token
    """
    content = request.get_json(silent=True)

    if not content.get("signupType"):
        return build_response.build_json({"status":False, "error": 'SignUp Type is missing.'})

    if content.get("signupType") != 1:
        return build_response.build_json({"status":False, "error": 'SignUp Type is wrong.'})

    email = content.get("email")

    user = User.objects(email=email).first()
    
    '''
    If user exit return the error: User lready exist
    '''
    if not user:
        user = User()
    else:
        return build_response.build_json({"status":False, "error": 'Email already exist.'})


    try:
        save_response = save_user(user)
        if 'error' in save_response:
            raise Exception(save_response['error'])
        else:
            user = User.objects.get(id=ObjectId(save_response['user_id']))
            return build_response.build_json(
                {
                    'status':True,
                    'membership': 'Free' if user.membershipPlan == 0 else 'Paid',
                    'auth_token': create_jwttoken(1,user.email)[1].decode('utf-8')
                }
            )
    except Exception as e:
        return build_response.build_json({"status":False, "error": str(e)})

@auth.route('/socialsignup', methods=['POST'])
def soical_signup():
    """
    Social SignUp and return a token
    """
    content = request.get_json(silent=True)

    #Signup Type and Social Id is required
    if not (content.get("socialId") or content.get("signupType")):
        return build_response.build_json({"status":False, "error": 'Social Id or SignUp Type is missing.'})

    #check for valid signup type value
    if content.get("signupType") not in [2,3,4,5]:
        return build_response.build_json({"status":False, "error": 'SignUp Type is not a valid value.'})

    
    signupType = content.get("signupType")
    socialId = content.get("socialId")

    #check of alreay exist user
    #First By Email
    if content.get("email"):
        email = content.get("email")
        user = User.objects(email=email).first()

    #If no user By email then try By Social Id
    try:
        user
    except NameError:
        user = getUserBySoicalId(signupType, socialId)
    else:
        if not user:
            user = getUserBySoicalId(signupType, socialId)

        
    #If no user exist, try to register as new
    if not user:
        #No address info not provided
        #return the response and ask for address info along with all signup info
        if not (content.get("countryCode") and content.get("state")):
            return build_response.build_json({"status":False, "error": 'Country code and State are required.'})
        else:
            #Register new user return the token
            user = User()
    try:
        save_response = save_user(user)
        if 'error' in save_response:
            raise Exception(save_response['error'])
        else:
            return build_response.build_json(
                {
                    'status':True,
                    'membership': 'Free' if user.membershipPlan == 0 else 'Paid',
                    'auth_token': create_jwttoken(signupType,socialId)[1].decode('utf-8')
                }
            )
    except Exception as e:
        return build_response.build_json({"status":False, "error": str(e)})


@auth.route('/profile')
@login_required
def profile():
    user = g.user
    return build_response.build_json(
        {
            'status':True,
            'profile':transpose_user(user)
        }
    )

@auth.route('/profile', methods=['POST'])
@login_required
def update_profile():
    user = g.user
    content = request.get_json(silent=True)
    user.firstName = content.get("firstName")
    user.lastName = content.get("lastName")

    if content.get("email") and content.get("email") != user.email:
        if User.objects(email=content.get("email")):
            return build_response.build_json({"status":False, "error": 'Email already exist.'})
        else:
            user.email = content.get("email")

    try:
        user_id = user.save()
        return build_response.build_json(
            {
                'status':True,
                'membership': 'Free' if user.membershipPlan == 0 else 'Paid',
                'auth_token': create_jwttoken(1,user.email)[1].decode('utf-8')
            }
        )
    except Exception as e:
        return build_response.build_json({"status":False, "error": str(e)})

@auth.route('/changepassword', methods=['POST'])
@login_required
def change_password():
    user = g.user
    content = request.get_json(silent=True)

    newPassword = content.get("newPassword")
    oldPassword = content.get("oldPassword")
    
    
    
    if not check_password_hash(user.password, oldPassword):
        return build_response.build_json({"status":False, "error": 'Old password is incorrect.'})

    user.password = generate_password_hash(newPassword)

    try:
        user.save()
        return build_response.build_json(
            {
                'status':True,
                'message': 'Password has updated'
            }
        )
    except Exception as e:
        return build_response.build_json({"status":False, "error": str(e)})