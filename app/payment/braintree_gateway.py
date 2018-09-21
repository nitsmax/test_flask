from flask import current_app as app
from flask import request, g
import braintree

class BraintreeGateway():

	def __init__(self):
		self.gateway = braintree.BraintreeGateway(
		    braintree.Configuration(
		        environment=app.config.get('BT_ENVIRONMENT'),
		        merchant_id=app.config.get('BT_MERCHANT_ID'),
		        public_key=app.config.get('BT_PUBLIC_KEY'),
		        private_key=app.config.get('BT_PRIVATE_KEY')
		    )
		)

	def generate_client_token(self):
		try:
			response = self.gateway.client_token.generate()
			return {'status': True,'result': response}
		except Exception as e:
			return {'status': False,'message': str(e)}

	def create_customer(self, options):
		try:
			response = self.gateway.customer.create(options)
			return {'status': True,'result': response}
		except Exception as e:
			return {'status': False,'message': str(e)}

	def transact(self,options):
		try:
			response = self.gateway.transaction.sale(options)
			return {'status': True,'response': response}
		except Exception as e:
			return {'status': False,'message': str(e)}

	def find_transaction(self,id):
		try:
			response = self.gateway.transaction.find(id)
			return {'status': True,'response': response}
		except Exception as e:
			return {'status': False,'message': str(e)}

	def subscription(self, options):
		try:
			response = self.gateway.subscription.create(options)
			return {'status': True,'response': response}
		except Exception as e:
			return {'status': False,'message': str(e)}