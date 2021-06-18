from flask import Blueprint
from flask_restful import Api

from api.endpoints.datamarts import Datamarts
from api.endpoints.datamarts.ingestion import *
from api.endpoints.datamarts.creation import *

DATAMARTS_BLUEPRINT = Blueprint("datamarts.py", __name__)

datamarts_routes = ["/datamarts", "/datamarts/<uid>"]
Api(DATAMARTS_BLUEPRINT).add_resource(Datamarts, *datamarts_routes)

# ===== ingestion ==================================================================================
mongodb_ingestion_routes = ["/workspaces/<workspace_id>/datamarts/ingestion/mongodb"]
Api(DATAMARTS_BLUEPRINT).add_resource(MongodbIngestion, *mongodb_ingestion_routes)

postgresql_ingestion_routes = ["/workspaces/<workspace_id>/datamarts/ingestion/postgresql"]
Api(DATAMARTS_BLUEPRINT).add_resource(PostgresqlIngestion, *postgresql_ingestion_routes)

csv_ingestion_routes = ["/workspaces/<workspace_id>/datamarts/ingestion/csv"]
Api(DATAMARTS_BLUEPRINT).add_resource(CsvIngestion, *csv_ingestion_routes)

json_ingestion_routes = ["/workspaces/<workspace_id>/datamarts/ingestion/json"]
Api(DATAMARTS_BLUEPRINT).add_resource(JsonIngestion, *json_ingestion_routes)

xml_ingestion_routes = ["/workspaces/<workspace_id>/datamarts/ingestion/xml"]
Api(DATAMARTS_BLUEPRINT).add_resource(XmlIngestion, *xml_ingestion_routes)

# ===== creation ===================================================================================
creation_preview_routes = ["/datamarts/creation/preview"]
Api(DATAMARTS_BLUEPRINT).add_resource(DatamartPreviewApi, *creation_preview_routes)

creation_save_routes = ["/datamarts/creation/save"]
Api(DATAMARTS_BLUEPRINT).add_resource(DatamartSaveApi, *creation_save_routes)
