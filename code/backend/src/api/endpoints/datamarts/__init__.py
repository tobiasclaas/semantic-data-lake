import json

from flask import jsonify, Response
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from flask_restful.reqparse import Argument

from api.services.decorators import parse_params
from business_logic.services.mapper import mapper
from database.data_access import datamart_data_access as data_access
from business_logic.spark import SparkHelper


class Datamarts(Resource):
    
    @parse_params(
        Argument("page", default=1, type=int, required=False),
        Argument("limit", default=10, type=int, required=False),
        Argument("field_to_order", default="created_at", type=str, required=False),
        Argument("asc", default=False, type=bool, required=False),
        Argument("search", default=None, type=str, required=False),
        Argument("uid", default=None, type=str, required=False),
    )
    def get(self, workspace_id, uid, page, limit, field_to_order, asc, search):
        if uid is None:
            print("uid is none")
            result = []
            datamarts = data_access.get_list(page, limit, field_to_order, asc, search)
            
            for datamart in datamarts.items:
                if mapper(datamart)['workspace_id'] == workspace_id:
                    result.append(mapper(datamart))

            return jsonify(result)
        else:
            return jsonify(mapper(data_access.get_by_uid(uid)))

    
    @parse_params(
        Argument("uid", type=str, required=True),
    )
    def delete(self, workspace_id, uid):
        datamart = data_access.get_by_uid(uid)
        hnr = datamart.human_readable_name
        datamart.delete()
        return f"deleted datamart {hnr}"

    
    @parse_params(
        Argument("comment", default='', type=str, required=False),
        Argument("annotated_schema", required=False),
        Argument("human_readable_name", required=False),
    )
    def put(self, workspace_id, uid, comment, annotated_schema, human_readable_name):
        datamart = data_access.get_by_uid(uid)
        datamart.human_readable_name = human_readable_name
        datamart.workspace_id = workspace_id
        datamart.comment = comment
        datamart.metadata.schema = annotated_schema\
            .replace("\'", "\"")\
            .replace(" ", "")\
            .replace("True", "true")\
            .replace("False", "false")
        datamart.save()
        return jsonify(mapper(datamart))
