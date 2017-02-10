
import os

DEBUG = os.getenv('DEBUG', 'True')
if DEBUG.lower() == 'true':
	DEBUG = True

elif DEBUG.lower() == 'false':
	DEBUG = False



# MONGODB
MONGO_URI = os.getenv('MONGO_URI', '')


# Email
MANDRILL_API_KEY = os.getenv('MANDRILL_API_KEY', '')


# S3
S3_ACCESS_KEY = os.getenv('S3_ACCESS_KEY', '')
S3_SECRET_KEY = os.getenv('S3_SECRET_KEY', '')
S3_BUCKET = os.getenv('S3_BUCKET', 'core')


# CELERY
CELERY_BROKER_URL =	os.getenv('CELERY_BROKER_URL', '')
CELERY_RESULT_BACKEND =	os.getenv('CELERY_RESULT_BACKEND', '')
CELERY_SEND_TASK_ERROR_EMAILS = False


# ELASTICSEARCH
ELASTICSEARCH_HOST = os.getenv('ELASTICSEARCH_HOST', '')
ELASTICSEARCH_USER = os.getenv('ELASTICSEARCH_USER', '')
ELASTICSEARCH_PASSWORD = os.getenv('ELASTICSEARCH_PASSWORD', '')

