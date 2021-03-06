
from core import app
from core.models.core.has_routes import HasRoutes

from flask import request

from bson.objectid import ObjectId
from werkzeug import secure_filename

import mimetypes
import boto

from core.models.auth.drive import Drive




with app.app_context():
	class Upload(HasRoutes):

		endpoint = '/_upload'
		routes = [
			{
				'route': '',
				'view_function': 'upload_view',
				'methods': ['POST']
			}
		]

		@classmethod
		def upload_view(cls):
			drive = Drive.get_where({'shop': request.form.get('shop')})
			uploaded_file = request.files['file']

			_id = str(ObjectId())

			connection = boto.connect_s3(app.config['S3_ACCESS_KEY'], app.config['S3_SECRET_KEY'])
			bucket = connection.get_bucket(app.config['S3_BUCKET'])

			key = bucket.new_key('uploads/' + _id)
			key.set_contents_from_file(uploaded_file, headers={}, policy='public-read')

			return cls._format_response({
				'_id': _id
			})


			





