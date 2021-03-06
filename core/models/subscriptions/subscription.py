
from core import app
from flask import request, abort

from core.helpers.json import to_json
from core.models.core.model import Model
from core.models.core.has_routes import HasRoutes

from core.helpers.validation_rules import validation_rules

from bson.objectid import ObjectId

import stripe
import shopify


with app.app_context():
	class Subscription(HasRoutes, Model):

		collection_name = 'subscriptions'

		schema = {
			'token': validation_rules['text'],
			'plans': {
				'type': 'list',
				'schema': {
					'type': 'dict',
					'schema': {
						'plan': validation_rules['text'],
						'quantity': validation_rules['int']
					}
				}
			},
			'order_id': validation_rules['text'],
			'customer_id': validation_rules['text'],
			'metadata': validation_rules['metadata']
		}


		endpoint = '/subscriptions'
		routes = [
			# {
			# 	'route': '',
			# 	'view_function': 'list_view',
			# 	'methods': ['GET']
			# },
			{
				'route': '',
				'view_function': 'create_view',
				'methods': ['POST']
			},
			# {
			# 	'route': '/<ObjectId:_id>',
			# 	'view_function': 'get_view',
			# 	'methods': ['GET']
			# },
			{
				'route': '/<ObjectId:_id>',
				'view_function': 'update_view',
				'methods': ['PATCH', 'PUT']
			},
			{
				'route': '/create_order',
				'view_function': 'create_order_view',
				'methods': ['GET', 'POST']
			},
			# {
			# 	'route': '/<ObjectId:_id>',
			# 	'view_function': 'delete_view',
			# 	'methods': ['DELETE'],
			# 	'requires_admin': True
			# }
		]



		@classmethod
		def create(cls, document):

			customer = app.stripe.Customer.create(
				source=document['token']
			)
			document['stripe_id'] = customer['id']


			return super().create(document)



		@classmethod
		def update(cls, _id, document, other_operators={}, projection={}):


			document = super().update(_id, document, other_operators, projection)


			try:
				if document['order_id']:
					app.stripe.Subscription.create(
						customer=document['stripe_id'],
						items=document['plans'],
						coupon='first-free',
						metadata={'order_id': document['order_id'], 'customer_id': document['customer_id']}
					)
			except KeyError:
				pass



			return document



		@classmethod
		def preprocess(cls, document):


			return super().preprocess(document)



		@classmethod
		def postprocess(cls, document):


			return document



		@classmethod
		def create_order_view(cls):
			json = cls._get_json_from_request()
			invoice = json['data']['object']


			shopify.ShopifyResource.set_site("https://%s:%s@wisecare.myshopify.com/admin" % (app.config['SHOPIFY_API_KEY'], app.config['SHOPIFY_PASSWORD']))

			order = shopify.Order()
			order.customer = {
				'id': invoice['lines']['data'][0]['metadata']['customer_id']
			}
			order.send_receipt = True
			order.use_customer_default_address = True
			order.line_items = []
			for line in invoice['lines']['data']:
				order.line_items.append({'title': line['plan']['name'].split(' - ')[0], 'product_id': line['plan']['id'].split('-')[0], 'quantity': line['quantity'], 'price': str(line['amount']/100)})
			order.note_attributes = [{'invoice_id': invoice['id']}]
			order.source_name = 'subscriptions'

			order.save()



			return cls._format_response({})



