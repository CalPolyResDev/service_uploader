from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

INTERNAL_URL = 'http://localhost:8000/'

DATABASES['dw']['NAME'] = 'dwtstdb.db.calpoly.edu:1521/dwtstdb'
