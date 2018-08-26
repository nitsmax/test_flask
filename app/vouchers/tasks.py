import os
from flask import request, g, url_for
from flask import current_app as app
from app.vouchers.models import Voucher
from app.users.models import MembershipPlan
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import jwt


def save_voucher(voucher):

    voucher.name = request.form['name']
    voucher.code = request.form['code']

    if request.form.get("uselimit"):
        voucher.uselimit = request.form['uselimit']

    if request.form.get("description"):
        voucher.description = request.form['description']

    if request.form.get("expireDate"):
        voucher.expireDate = request.form['expireDate']

    MembershipP = MembershipPlan.objects(name=request.form['membershipPlan']).get()
    if MembershipP:
        voucher.MembershipPlan = MembershipP

    voucher.status = 1
    try:
        voucher_id = voucher.save()
        return {'voucher_id': str(voucher_id.id)}
    except Exception as e:
        return {'error': str(e)}

def transpose_voucher(voucher):
    return {
        '_id': str(voucher.id),
        'firstName': voucher.firstName,
        'lastName': voucher.lastName,
        'fullName': voucher.firstName+' '+voucher.lastName,
        'email': voucher.email,
        'Membership': voucher.membershipPlan.name if voucher.membershipPlan else '',
        'memberShipExpDate': voucher.memberShipExpDate.isoformat() if voucher.memberShipExpDate else '',
        'date_created': voucher.date_created.isoformat(),
        'date_modified': voucher.date_modified.isoformat()
    }
