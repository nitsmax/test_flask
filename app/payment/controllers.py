import os
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import Blueprint, request, Response
from flask import current_app as app
from app.commons import build_response
from app.users.models import User
from app.commons.utils import update_document
from werkzeug.security import generate_password_hash, check_password_hash
from app.auth.models import login_required


payment = Blueprint('payment_blueprint', __name__,
                    url_prefix='/api/payment')


@payment.route('/checkout')
@login_required
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

