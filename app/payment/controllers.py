import os
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import Blueprint, request, Response, g
from flask import current_app as app
from app.commons import build_response
from app.auth.models import login_required
import json
from app.payment.tasks import PaymentRepo
from app.vouchers.models import Voucher
import datetime
from decimal import Decimal

payment = Blueprint('payment_blueprint', __name__,
                    url_prefix='/api/payment')


@payment.route('/checkout')
@login_required
def checkout():
    try:
        user = g.user
        if not user.country:
            raise Exception('Some thing went wrong')

        payment_repo = PaymentRepo()

        client_token = payment_repo.bt_generate_client_token()

        if 'error' in client_token:
            raise Exception('Some thing went wrong')

        membership_plan = {
            'id': str(user.country.id),
            'amount': float(round(user.country.monthlyAmount)),
            'currency': user.country.countryCurrency,
            'frequency': 'Monthly'
        }

        return build_response.build_json(
            {
                'status':True,
                'braintree_token': client_token['client_token'],
                'membership_plan': membership_plan
            }
        )
    except Exception as e:
        return build_response.build_json({"status":False, "error": str(e)})

@payment.route('/checkout', methods=['POST'])
@login_required
def post_checkout():
    #Insert to Subscription
    '''
    {
        "payment_method_payload": {
            "nonce":"tokencc_bj_t68pp6_8h2y94_xfc3mm_j53prf_ph7",
            "details":{
                "cardType":"Visa",
                "lastFour":"1111",
                "lastTwo":"11"
            },
            "type":"CreditCard",
            "description":"ending in 11",
            "binData":{
                
            }
        },
        "amount": 150,
        "voucher_code": "GET50", #leave blank if not applied,
        "gateway": "Braintree"
    }
    '''
    try:
        content = request.get_json(silent=True)

        payment_repo = PaymentRepo()

        subscription = payment_repo.create_subscription()
        if 'error' in subscription:
            raise Exception(subscription['error'])

        if not subscription['success']:
            raise Exception('Payment Failed: '+subscription['error'])

        response = {
            'status': True,
            'subscription_id': subscription['subscription_id'],
            'message': 'Payment Successful'
        }
        return build_response.build_json(response)
    except Exception as e:
        return build_response.build_json({"status":False, "error": 'Payment Failed'})
        
@payment.route('/apply_voucher', methods=['POST'])
@login_required
def apply_voucher():
    '''
    {
        "voucher_code": "GET25"
    }
    '''
    content = request.get_json(silent=True)
    user = g.user
    membershipPlan = user.country

    try:
        voucher = Voucher.objects(code__exact=content.get('voucher_code'))
        
        if not voucher:
            raise Exception('Not Exist:Invalid Token')

        voucher = voucher.get()

        if (voucher.uselimit - voucher.usedNum) <= 0:
            raise Exception('Invalid Token')

        '''
        if voucher.expireDate and voucher.expireDate < datetime.datetime.utcnow:
            raise Exception('Invalid Token')

        '''

        if membershipPlan not in voucher.membershipPlan:
            raise Exception('Invalid Token')

        amount = Decimal(membershipPlan.monthlyAmount - (membershipPlan.monthlyAmount*voucher.discount)/100)
        
        response = {
            'status': True,
            'voucher_code': voucher.code,
            'voucher_discount': str(round(voucher.discount))+'%',
            'voucher_title': voucher.name,
            'amount': float(round(amount,2)),
            'currency': membershipPlan.countryCurrency,
            'frequency': 'Monthly'
        }
        return build_response.build_json(response)
    except Exception as e:
        return build_response.build_json({"status":False, "error": str(e)})
        
