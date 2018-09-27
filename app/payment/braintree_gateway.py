from flask import current_app as app
from flask import request, g
import braintree

class BraintreeGateway():

	def __init__(self,config):
		self.gateway = braintree.BraintreeGateway(
		    braintree.Configuration(
		        environment = config['environment'],
		        merchant_id = config['merchant_id'],
		        public_key = config['public_key'],
		        private_key = config['private_key'],
		    )
		)

	def generate_client_token(self):
		try:
			client_token =  self.gateway.client_token.generate()
			return {'client_token': client_token}
		except Exception as e:
			return {'error': str(e)}

	def create_customer(self, options):
		try:
			customer = self.gateway.customer.create(options)
			return {'customer': customer}
		except Exception as e:
			return {'error': str(e)}

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
			subscription = self.gateway.subscription.create(options)
			return {'subscription' : subscription}
		except Exception as e:
			return {'error': str(e)}

	def cancel_subscription(self, subscriptionId):
		try:
			subscription = self.gateway.subscription.cancel(subscriptionId)
			return {'subscription' : subscription}
		except Exception as e:
			return {'error': str(e)}

	def parse_errors(self, errorObject):
		if errorObject.errors and len(errorObject.errors.deep_errors):
			error = errorObject.errors.deep_errors[0]
			errMessage = error.message
			errCode = error.code
			validationError = True
		else:
			pass

