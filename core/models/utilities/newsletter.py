
from core import app
from core.models.core.has_routes import HasRoutes

from core.models.auth.chimp import Chimp

from core.helpers.validation_rules import validation_rules
from core.helpers.json import to_json

from flask import request
from mailchimp3 import MailChimp



with app.app_context():
	class Newsletter(HasRoutes):

		endpoint = '/_newsletter'
		routes = [
			{
				'route': '/signup',
				'view_function': 'signup_view',
				'methods': ['POST']
			}
		]

		schema = {
			'email': validation_rules['email'],
			'shop': validation_rules['text']
		}


		@classmethod
		def signup_view(cls):
			data = cls.validate(cls._get_json_from_request())

			chimp = Chimp.get_where({'shop': data['shop']})
			client = MailChimp(chimp['username'], chimp['access_token'])

			try:
				response = client.lists.members.create(chimp['list_id'], {
					'email_address': data['email'],
					'status': 'subscribed'
				})

				return cls._format_response({
					'email': data['email'],
					'list_id': chimp['list_id'],
				})

			except Exception as e:
				return to_json({
					'email': data['email'],
					'list_id': chimp['list_id'],
					'error': e.response.json()['title']
				}, 400)

