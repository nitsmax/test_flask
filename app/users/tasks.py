import os
from flask import request, g, url_for
from flask import current_app as app
from app.users.models import User, MembershipPlan
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import jwt


def save_user(user):

    content = request.get_json(silent=True)

    #existing user not update the data
    if not user.id:
        user.firstName = content.get("firstName")
        user.countryCode = content.get("countryCode")
        user.state = content.get("state")
        
    signupType = content.get("signupType")    
    user.signupType = signupType
    user.status = 1

    if content.get("email"):
        user.email = content.get("email")

    if content.get("lastName"):
        user.lastName = content.get("lastName")

    if content.get("phoneNumber"):
        user.phoneNumber = content.get("phoneNumber")

    if content.get("password"):
        user.password = generate_password_hash(content.get("password"))

    if content.get("city"):
        user.city = content.get("city")

    if content.get("zipcode"):
        user.zipcode = content.get("zipcode")

    if content.get("socialId") and signupType != 1:
        socialId = content.get("socialId")

        if signupType == 2:
            user.facebookId = socialId
        elif signupType == 3:
            user.twitterId = socialId
        elif signupType == 4:
            user.googleId = socialId
        elif signupType == 5:
            user.snapchatId = socialId


    user.userType = 'User'
    
    MembershipP = MembershipPlan.objects(name='Free').get()
    if MembershipP:
        user.MembershipPlan = MembershipP
    
    print(user.MembershipPlan.name)
    try:
        user_id = user.save()
        return {'user_id': str(user_id.id)}
    except Exception as e:
        return {'error': str(e)}

def transpose_user(user):
	return {
        '_id': str(user.id),
        'firstName': user.firstName,
        'lastName': user.lastName,
        'fullName': user.firstName+' '+user.lastName,
        'email': user.email,
        'Membership': user.membershipPlan.name if user.membershipPlan else '',
        'memberShipExpDate': user.memberShipExpDate.isoformat() if user.memberShipExpDate else '',
        'date_created': user.date_created.isoformat(),
        'date_modified': user.date_modified.isoformat()
    }

def create_jwttoken(signupType,fieldValue):
    if signupType == 2:
        field = 'facebookId'
    elif signupType == 3:
        field = 'twitterId'
    elif signupType == 4:
        field = 'googleId'
    elif signupType == 5:
        field = 'snapchatId'
    else:
        field = 'email'
    exp = datetime.datetime.utcnow() + datetime.timedelta(hours=app.config['TOKEN_EXPIRE_HOURS'])
    auth_token = jwt.encode({field: fieldValue, 'exp': exp},
                         app.config['KEY'], algorithm='HS256')

    refresh_token = jwt.encode({field: fieldValue},
                         app.config['KEY'], algorithm='HS256')

    return [auth_token, refresh_token]

def getUserBySoicalId(signupType, socialId):
    if signupType == 2:
        return User.objects(facebookId=socialId).first()
    elif signupType == 3:
        return User.objects(twitterId=socialId).first()
    elif signupType == 4:
        return User.objects(googleId=socialId).first()
    elif signupType == 5:
        return User.objects(snapchatId=socialId).first()