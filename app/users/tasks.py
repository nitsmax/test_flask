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

    user.email = content.get("email")
    user.firstName = content.get("firstName")
    user.lastName = content.get("lastName")

    if content.get("phoneNumber"):
        user.phoneNumber = content.get("phoneNumber")

    if content.get("password"):
        user.password = generate_password_hash(content.get("password"))

    if content.get("countryCode"):
        user.countryCode = content.get("countryCode")

    if content.get("state"):
        user.state = content.get("state")

    if content.get("city"):
        user.city = content.get("city")

    if content.get("zipcode"):
        user.zipcode = content.get("zipcode")

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

def create_jwttoken(email):
    exp = datetime.datetime.utcnow() + datetime.timedelta(hours=app.config['TOKEN_EXPIRE_HOURS'])
    auth_token = jwt.encode({'email': email, 'exp': exp},
                         app.config['KEY'], algorithm='HS256')

    refresh_token = jwt.encode({'email': email},
                         app.config['KEY'], algorithm='HS256')

    return [auth_token, refresh_token]