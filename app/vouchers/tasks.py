import os
from flask import request, g, url_for
from flask import current_app as app
from app.vouchers.models import Voucher
from app.countries.models import Country
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import jwt


def save_voucher(voucher):

    voucher.name = request.form['name']
    voucher.code = request.form['code']
    voucher.discount = request.form['discount']

    if request.form.get("uselimit"):
        voucher.uselimit = request.form['uselimit']

    if request.form.get("description"):
        voucher.description = request.form['description']

    if request.form.get("expireDate"):
        voucher.expireDate = request.form['expireDate']

    if request.form.get("membershipPlan"):
        country = Country.objects(id=request.form.get("membershipPlan")).get()
        if country:
            voucher.membershipPlan = [country]


    '''
    #Multi Member ship
    if request.form.getlist("membershipPlans"):

        membershipPlans = []

        for countryId in request.form.getlist("membershipPlans"):
            country = Country.objects(id=countryId).get()
            
            if country:
                membershipPlans.append(country)
        
        voucher.membershipPlan = membershipPlans

    '''

    try:
        voucher_id = voucher.save()
        return {'voucher_id': str(voucher_id.id)}
    except Exception as e:
        return {'error': str(e)}

def transpose_voucher(voucher):
    return {
        '_id': str(voucher.id),
        'name': voucher.name,
        'code': voucher.code,
        'discount': float(voucher.discount),
        'uselimit': voucher.uselimit,
        'description': voucher.description if voucher.description else '',
        'usedNum': voucher.usedNum,
        'expireDate': voucher.expireDate.isoformat() if voucher.expireDate else '',
        'membershipPlan': [country.CountryName for country in voucher.membershipPlan] if voucher.membershipPlan else [],
        'date_created': voucher.date_created.isoformat(),
        'date_modified': voucher.date_modified.isoformat()
    }
