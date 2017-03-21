
from core import app
from flask import request, abort

from core.helpers.json import to_json
from core.models.core.model import Model

from bson.objectid import ObjectId

import string
import random
import hashlib
import uuid



with app.app_context():
	class Drive(Model):

		collection_name = 'drives'



		@classmethod
		def create(cls, document):


			return super().create(document)





		@classmethod
		def preprocess(cls, document):


			return super().preprocess(document)



		@classmethod
		def postprocess(cls, document):


			return document



