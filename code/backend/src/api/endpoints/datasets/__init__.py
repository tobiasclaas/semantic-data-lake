import json

from flask import jsonify, Response, request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from flask_restful.reqparse import Argument
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import BadRequest

from api.services.decorators import parse_params
from business_logic.services.mapper import mapper
from database.data_access import dataset_data_access
from business_logic.spark import SparkHelper
import pyspark.sql.functions as f

def mapper(item):
    return{
        "id": str(item.id),
        "name": item.name,
        "type": item.type
    }

class Datasets(Resource):
    def get(self, workspace_id):
        return jsonify([mapper(item) for item in dataset_data_access.get_all(workspace_id)])

    @parse_params( 
        Argument("type", default=None, type=str, required=True),
    )
    def post(self, type, workspace_id):
        if (type == "csv"):
            return jsonify(mapper(dataset_data_access.add_csv(request.form["name"], request.files["file"], request.form["delimiter"], bool(int(request.form["has_header"])) , workspace_id)))
        return BadRequest()
