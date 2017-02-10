from core import app
from core import celery
from flask import request, abort, json

from core.helpers.json import json_formater


@celery.task(name='search_index')
def search_index(type, id, body):

	# app.search.index(index='available', doc_type=type, body=json.dumps(body, sort_keys=False, default=json_formater), id=str(id))
	pass



@celery.task(name='search_delete')
def search_delete(type, id):
	
	# app.search.delete(index='available', doc_type=type, id=str(id))
	pass
