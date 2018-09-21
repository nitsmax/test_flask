import os
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import Blueprint, request, Response
from flask import current_app as app
from app.commons import build_response
from app.users.models import User
from app.commons.utils import update_document, dumpObj
from werkzeug.security import generate_password_hash, check_password_hash
from app.auth.models import login_required
from app.payment.braintree_gateway import BraintreeGateway
import json
import pprint


payment = Blueprint('payment_blueprint', __name__,
                    url_prefix='/api/payment')


@payment.route('/checkout')
#@login_required
def checkout():
    try:
        bt = BraintreeGateway()
        response = bt.generate_client_token()

        if not response['status']:
            raise Exception('Some thing went wrong')

        return build_response.build_json(
                {
                    'status':True,
                    'braintree_token': response['result'],
                    'membership_plan': {
                        'id': '55a0f1d420a4d760b5fc043f',
                        'amount': 200,
                        'currency': 'INR',
                        'frequency': 'Monthly'
                    }
                }
            )
    except Exception as e:
        return build_response.build_json({"status":False, "error": str(e)})

@payment.route('/checkout', methods=['POST'])
@login_required
def post_checkout():
    try:
        bt = BraintreeGateway()

        response = bt.create_customer({
            "first_name": "Charity",
            "last_name": "Smith",
            "payment_method_nonce": "ake-valid-nonce",
        })

        for key in dir(response['result']):
            print('{}: {}'.format(key, getattr(response['result'], key)))

        #pprint.pprint(vars(response['result']))
        return build_response.sent_ok()

        if not response['status']:
            raise Exception('Some thing went wrong')


        if not response['result'].is_success:
            print(response['result'])
            return build_response.sent_ok()
            raise Exception('Some thing went wrong')


        response = bt.subscription({
            "payment_method_token": "fake-valid-nonce",
            "plan_id": "monthly_india",
            "price": 100 
        })
        print(response)
        return build_response.sent_ok()
    except Exception as e:
        return build_response.build_json({"status":False, "error": str(e)})

