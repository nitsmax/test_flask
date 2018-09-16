import os
from flask import request, g, url_for
from flask import current_app as app
from app.users.models import User
from app.countries.models import Country
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import jwt
import base64


def save_user(user):

    content = request.get_json(silent=True)

    #existing user not update the data
    if not user.id:
        user.firstName = content.get("firstName")
        user.countryCode = content.get("countryCode")
        country = Country.objects(CountryCode=content.get("countryCode")).get()
        if country:
            user.country = country
        user.state = content.get("state")
        
    signupType = content.get("signupType")    
    user.signupType = signupType

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
        'country': user.country.CountryName if user.country else '',
        'state': user.state,
        'membershipPlan': user.membershipPlan,
        'memberShipExpDate': user.memberShipExpDate.isoformat() if user.memberShipExpDate else '',
        'date_created': user.date_created.isoformat(),
        'date_modified': user.date_modified.isoformat()
    }

def getUserBySoicalId(signupType, socialId):
    if signupType == 2:
        return User.objects(facebookId=socialId).first()
    elif signupType == 3:
        return User.objects(twitterId=socialId).first()
    elif signupType == 4:
        return User.objects(googleId=socialId).first()
    elif signupType == 5:
        return User.objects(snapchatId=socialId).first()