import os
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import Blueprint, request, Response
from flask import current_app as app
from app.commons import build_response
from app.users.models import User
from app.users.tasks import save_user, transpose_user, create_jwttoken,getUserBySoicalId
from app.commons.utils import update_document
from werkzeug.security import generate_password_hash, check_password_hash


payment = Blueprint('payment_blueprint', __name__,
                    url_prefix='/api/payment')


@payment.route('/checkout')
def checkout():
    return build_response.build_json(
            {
                'status':True,
                'braintree_token': 'eyJ2ZXJzaW9uIjoyLCJhdXRob3JpemF0aW9uRmluZ2VycHJpbnQiOiJlMTFlZWQ4ZDZjNWYzYTI0YmJlNmUyNmRkMGU3OTE1OWExYzI1YmIyNDMxMWFkM2QxOWM1ZmZmNzNkOTUxZGFjfGNyZWF0ZWRfYXQ9MjAxOC0wOS0xNlQwNToyNjozMi4zOTQ5NzE0ODErMDAwMFx1MDAyNm1lcmNoYW50X2lkPXBzajh4eGs1N3hwaDdmd21cdTAwMjZwdWJsaWNfa2V5PWdqcXJreTV5ejR5ZDcycGIiLCJjb25maWdVcmwiOiJodHRwczovL2FwaS5zYW5kYm94LmJyYWludHJlZWdhdGV3YXkuY29tOjQ0My9tZXJjaGFudHMvcHNqOHh4azU3eHBoN2Z3bS9jbGllbnRfYXBpL3YxL2NvbmZpZ3VyYXRpb24iLCJjaGFsbGVuZ2VzIjpbImN2diIsInBvc3RhbF9jb2RlIl0sImVudmlyb25tZW50Ijoic2FuZGJveCIsImNsaWVudEFwaVVybCI6Imh0dHBzOi8vYXBpLnNhbmRib3guYnJhaW50cmVlZ2F0ZXdheS5jb206NDQzL21lcmNoYW50cy9wc2o4eHhrNTd4cGg3ZndtL2NsaWVudF9hcGkiLCJhc3NldHNVcmwiOiJodHRwczovL2Fzc2V0cy5icmFpbnRyZWVnYXRld2F5LmNvbSIsImF1dGhVcmwiOiJodHRwczovL2F1dGgudmVubW8uc2FuZGJveC5icmFpbnRyZWVnYXRld2F5LmNvbSIsImFuYWx5dGljcyI6eyJ1cmwiOiJodHRwczovL29yaWdpbi1hbmFseXRpY3Mtc2FuZC5zYW5kYm94LmJyYWludHJlZS1hcGkuY29tL3Bzajh4eGs1N3hwaDdmd20ifSwidGhyZWVEU2VjdXJlRW5hYmxlZCI6dHJ1ZSwicGF5cGFsRW5hYmxlZCI6dHJ1ZSwicGF5cGFsIjp7ImRpc3BsYXlOYW1lIjoiSWNyZW9uIiwiY2xpZW50SWQiOm51bGwsInByaXZhY3lVcmwiOiJodHRwOi8vZXhhbXBsZS5jb20vcHAiLCJ1c2VyQWdyZWVtZW50VXJsIjoiaHR0cDovL2V4YW1wbGUuY29tL3RvcyIsImJhc2VVcmwiOiJodHRwczovL2Fzc2V0cy5icmFpbnRyZWVnYXRld2F5LmNvbSIsImFzc2V0c1VybCI6Imh0dHBzOi8vY2hlY2tvdXQucGF5cGFsLmNvbSIsImRpcmVjdEJhc2VVcmwiOm51bGwsImFsbG93SHR0cCI6dHJ1ZSwiZW52aXJvbm1lbnROb05ldHdvcmsiOnRydWUsImVudmlyb25tZW50Ijoib2ZmbGluZSIsInVudmV0dGVkTWVyY2hhbnQiOmZhbHNlLCJicmFpbnRyZWVDbGllbnRJZCI6Im1hc3RlcmNsaWVudDMiLCJiaWxsaW5nQWdyZWVtZW50c0VuYWJsZWQiOnRydWUsIm1lcmNoYW50QWNjb3VudElkIjoiaWNyZW9ucDJwIiwiY3VycmVuY3lJc29Db2RlIjoiVVNEIn0sIm1lcmNoYW50SWQiOiJwc2o4eHhrNTd4cGg3ZndtIiwidmVubW8iOiJvZmYifQ==',
                'membership_plan': {
                    'id': '55a0f1d420a4d760b5fc043f',
                    'amount': 200,
                    'currency': 'INR',
                    'frequency': 'Monthly'
                }
            }
        )

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
            'payment_token': create_jwttoken(1,user.email)[1].decode('utf-8')
        }
    )
    return build_response.build_json({'status':True, 'payment_token': create_jwttoken(1,email)[1].decode('utf-8')})

@payment.route('/signup', methods=['POST'])
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
                    'payment_token': create_jwttoken(1,user.email)[1].decode('utf-8')
                }
            )
    except Exception as e:
        return build_response.build_json({"status":False, "error": str(e)})

@payment.route('/socialsignup', methods=['POST'])
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
                    'payment_token': create_jwttoken(signupType,socialId)[1].decode('utf-8')
                }
            )
    except Exception as e:
        return build_response.build_json({"status":False, "error": str(e)})