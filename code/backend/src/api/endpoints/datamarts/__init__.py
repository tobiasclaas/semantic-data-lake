from flask import jsonify
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from flask_restful.reqparse import Argument

from api.services.decorators import parse_params
from business_logic.services.mapper import mapper
from database.data_access import datamart_data_access as data_access


class Datamarts(Resource):
    @jwt_required
    @parse_params(
        Argument("page", default=1, type=int, required=False),
        Argument("limit", default=10, type=int, required=False),
        Argument("field_to_order", default="created_at", type=str, required=False),
        Argument("asc", default=False, type=bool, required=False),
        Argument("search", default=None, type=str, required=False)
    )
    def get(self, page, limit, field_to_order, asc, search, uid=None):
        if uid is None:
            result = []
            datamarts = data_access.get_list(page, limit, field_to_order, asc, search)

            for datamart in datamarts.items:
                result.append(mapper(datamart))

            return jsonify({
                "total": datamarts.total,
                "datamarts": result
            })
        else:
            return jsonify(mapper(data_access.get_by_uid(uid)))

    @jwt_required
    def delete(self, uid):
        datamart = data_access.get_by_uid(uid)
        hnr = datamart.human_readable_name
        datamart.delete()
        return f"deleted datamart {hnr}"

    @jwt_required
    @parse_params(
        Argument("comment", default='', type=str, required=False),
        Argument("annotated_schema", required=False),
        Argument("human_readable_name", required=False),
    )
    def put(self, uid, comment, annotated_schema, human_readable_name):
        datamart = data_access.get_by_uid(uid)
        datamart.human_readable_name = human_readable_name
        datamart.comment = comment
        datamart.metadata.schema = annotated_schema\
            .replace("\'", "\"")\
            .replace(" ", "")\
            .replace("True", "true")\
            .replace("False", "false")
        datamart.save()
        return jsonify(mapper(datamart))
