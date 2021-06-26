import json

from flask import jsonify, Response
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from flask_restful.reqparse import Argument

from api.services.decorators import parse_params
from business_logic.services.mapper import mapper
from database.data_access import datamart_data_access as data_access
from business_logic.spark import SparkHelper
import pyspark.sql.functions as f
from database.models import Job


class Jobs(Resource):
    @parse_params(
        # Argument("page", default=1, type=int, required=False),
        # Argument("limit", default=10, type=int, required=False),
        # Argument("field_to_order", default="created_at", type=str, required=False),
        # Argument("asc", default=False, type=bool, required=False),
        # Argument("search", default=None, type=str, required=False),
        Argument("id", default=None),
    )
    def get(self, id):
        if id is None:
            jobs = Job.objects.all()
            response = []
            for job in jobs:
                response.append(mapper(job))

            return jsonify({
                "total": datamarts.total,
                "datamarts": result
            })
        else:
            return jsonify(mapper(data_access.get_by_uid(uid)))
