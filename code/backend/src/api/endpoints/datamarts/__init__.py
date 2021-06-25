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
    @jwt_required
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

            return jsonify({
                "total": len(result),
                "datamarts": result
            })
        else:
            return jsonify(mapper(data_access.get_by_uid(uid)))

    @jwt_required
    @parse_params(
        Argument("uid", type=str, required=True),
    )
    def delete(self, workspace_id, uid):
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

    @jwt_required
    @parse_params(
        Argument("op", type=str, required=True),
        Argument("mart1", type=str, required=True),
        Argument("mart2", default='', type=str, required=False),
    )
    def post(self, workspace_id, op, mart1, mart2):
        try:
            mart1 = json.loads(mart1)
            datamart = data_access.get_by_uid(mart1["uid"])
            spark_helper = SparkHelper(f"transform_{datamart.uid}")
            dataframe = spark_helper.read_datamart(datamart)

            if op == "select":
                dataframe = dataframe.select(*mart1["columns"]).toPandas()
                spark_helper.spark_session.stop()
                return Response(dataframe.to_json(orient="records"), mimetype='application/json')

            # if op == "filter":
            #     dataframe = dataframe.select(*mart1["columns"]).toPandas()
            #     spark_helper.spark_session.stop()
            #     # return jsonify(dataframe)
            #     return Response(dataframe.to_json(orient="records"), mimetype='application/json')

            if op == 'join':
                mart2 = json.loads(mart2)
                datamart2 = data_access.get_by_uid(mart2["uid"])
                dataframe2 = spark_helper.read_datamart(datamart2)
                if mart1['columns'][0] == mart2['columns'][0]:
                    dataframe = dataframe.join(dataframe2, mart1['columns'][0]).toPandas()
                    spark_helper.spark_session.stop()
                    return Response(dataframe.to_json(orient="records"), mimetype='application/json')

        except Exception as e:
            if (spark_helper):
                spark_helper.spark_session.stop()

            print(e)
