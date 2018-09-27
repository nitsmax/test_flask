import os
from bson.objectid import ObjectId
from flask import request, g, url_for
from flask import current_app as app
from werkzeug.utils import secure_filename
from app.payment.models import Subscription, Transaction
from app.vouchers.models import Voucher
from app.payment.braintree_gateway import BraintreeGateway

class PaymentRepo():
    def __init__(self):

        self.bt = BraintreeGateway({
            'environment': app.config.get('BT_ENVIRONMENT'),
            'merchant_id': app.config.get('BT_MERCHANT_ID'),
            'public_key' :app.config.get('BT_PUBLIC_KEY'),
            'private_key' :app.config.get('BT_PRIVATE_KEY')
        })

    def bt_generate_client_token(self):
        return self.bt.generate_client_token()

    def insert_subscription(self, content, user):
        subscription = Subscription()
        subscription.user = user
        subscription.membershipPlan = user.country
        subscription.paymentGateway = content.get('gateway')
        subscription.paymentMethod = content.get('payment_method_payload')['type']
        subscription.membershipAmount = user.country.monthlyAmount
        subscription.paymentAmount = content.get('amount')
        subscription.currency = user.country.countryCurrency
        subscription.paymentInfo = str(content.get('payment_method_payload')['details'])

        if content.get('voucher_code'):
            voucher = Voucher.objects(code__exact=content.get('voucher_code'))
            if voucher:
                subscription.voucher = voucher.get()
        
        try:    
            subscription = subscription.save()
            return str(subscription.id)
        except Exception as e:
            return {'error': str(e)}

    def create_subscription(self):
        try:
            content = request.get_json(silent=True)
            user = g.user
            gateway = content.get('gateway')

            subscription_id = self.insert_subscription(content,user)

            if 'error' in subscription_id:
                raise Exception(subscription_id['error'])
        
            if content.get('gateway') == 'Braintree':
                response = self.bt_create_subscription({
                    "customer":{
                        "first_name": user.firstName,
                        "last_name": user.lastName,
                        "email": user.email,
                        "payment_method_nonce": content.get('payment_method_payload')['nonce'],
                    },
                    "order_id": subscription_id,
                    "price": content.get('amount')
                })
            elif content.get('gateway') == 'Paytm':
                pass
            else:
                pass

            if 'error' in response:
                raise Exception(response['error'])

            if not response['success']:
                return response

            response_subscription_success = self.subscription_success(
                gateway,
                subscription_id,
                response['subscription']
            )
            if 'error' in response_subscription_success:
                raise Exception(response['error'])

            return {
                'success': True,
                'subscription_id': subscription_id
            }
        except Exception as e:
            return {'error': str(e)}

    def bt_create_subscription(self,option):
        try:
            customer = self.bt.create_customer(option['customer'])
            if 'error' in customer:
                raise Exception (customer['error'])

            if not customer['customer'].is_success:
                return {
                    'success': False,
                    'messsage': customer['customer'].message
                }

            response_payment_method = self.bt_get_payment_method(customer['customer'].customer)

            if 'error' in response_payment_method:
                raise Exception(response_payment_method['error'])


            response_subscription = self.bt.subscription({
                "payment_method_token": response_payment_method['payment_method'].token,
                "plan_id": "monthly_india",
                "price": option['price']
            })

            if 'error' in response_subscription:
                raise Exception (response_subscription['error'])

            subscription = response_subscription['subscription']

            if not subscription.is_success:
                return {
                    'success': False,
                    'messsage': subscription.message
                }

            return {
                'success': True,
                'subscription': subscription.subscription
            }
        except Exception as e:
            return {'error': str(e)}

    def bt_get_payment_method(self,customer):
        try:
            payment_method = customer.paypal_accounts[0]
            return {'payment_method': payment_method}
        except Exception as e:
            try:
                payment_method = customer.credit_cards[0]
                return {'payment_method': payment_method}
            except Exception as e:
                return {'error': str(e)}

    def subscription_success(self,gateway,subscription_id,subscription):
        try:
            db_sub = Subscription.objects.get(id=ObjectId(subscription_id))

            if gateway == 'Braintree':
                db_sub.subscriptionId = subscription.id
                db_sub.subscriptionPlan = subscription.plan_id
                db_sub.subscriptionStatus = 'Active'
                db_sub.subscriptionNextBillingDate = subscription.next_billing_date

            db_sub.save()

            if db_sub.voucher:
                voucher = db_sub.voucher
                voucher.usedNum = voucher.usedNum-1
                voucher.save()

            user = db_sub.user
            user.membershipPlan = 1
            user.memberShipExpDate = subscription.next_billing_date
            user.save()

            return {'success': True}
        except Exception as e:
            return {'error': str(e)}

    def cancel_subscription(self):
        try:
            user = g.user
            subscription = Subscription.objects(user=user)
            if not subscription:
                raise Exception("Not subscribed yet")

            subscription = subscription.get()
            if subscription.paymentGateway == 'Braintree':
                response_cancel_subscription = self.bt.cancel_subscription(subscription.subscriptionId)
            elif subscription.paymentGateway == 'Paytm':
                pass

            if 'error' in response_cancel_subscription:
                raise Exception(response_cancel_subscription['error'])

            return {'success': True}
        except Exception as e:
            return {'error': str(e)}

        