from flask_restplus import Api

from .preprocessing import api as preprocessing
from .clustering import api as clustering

api = Api(title='Marvin', version='0.0', description='Text insights')

api.add_namespace(preprocessing)
api.add_namespace(clustering)