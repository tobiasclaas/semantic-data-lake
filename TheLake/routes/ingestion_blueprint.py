from flask import Blueprint
from flask_restful import Api
from apis.ingestion import *

INGESTION_BLUEPRINT = Blueprint('ingestion', __name__)

routes = ['/ingestion/mongodb']
Api(INGESTION_BLUEPRINT).add_resource(
    MongoIngestion, *routes,
)

routes = ['/ingestion/postgres']
Api(INGESTION_BLUEPRINT).add_resource(
    PostgresIngestion, *routes,
)

routes = ['/ingestion/file']
Api(INGESTION_BLUEPRINT).add_resource(
    FileIngestion, *routes,
)