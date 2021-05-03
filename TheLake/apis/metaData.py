#coding: utf-8
from array import array
import json
import uuid

from pyspark.sql.dataframe import DataFrame, DataFrameNaFunctions
from spark import SparkHelper
from flask_restful import abort, Resource
from flask_restful.reqparse import Argument
from flask_restful.inputs import boolean
from services.decorators import parseParams
from bl.metaData import MetaDataBusinessLogic
from flask_jwt_extended import jwt_required, get_jwt_identity, get_csrf_token, current_user
from flask import jsonify
from db.metaData import MetaDataDatabase
from pyspark.sql import functions

class MetaData(Resource):
    bl = MetaDataBusinessLogic()
    db = MetaDataDatabase()

    @jwt_required
    @parseParams(
        Argument("page", default=1, type=int, required=False),
        Argument("limit", default=10, type=int, required=False),
        Argument("fieldToOrder", default="insertedAt", type=str, required=False),
        Argument("asc", default=False, type=boolean, required=False),
        Argument("search", default=None, type=str, required=False)
    )
    def get(self, page, limit, fieldToOrder, asc, search, uid=None):
        if uid == None:
            return jsonify(self.bl.getList(page, limit, fieldToOrder, asc, search))
        else:
            return jsonify(self.bl.get(uid))

    @jwt_required
    def delete(self, uid):
        if self.bl.delete(uid) == True:
            return "", 204
        else:
            abort(404, message="User with that email {} was not deleted".format(uid))

    @jwt_required
    @parseParams(
        Argument("comment", default='', type=str, required=False),
        Argument("annotatedSchema", required=False),
        Argument("humanReadableName", required=False),
    )
    def put(self, uid, comment, annotatedSchema, humanReadableName):
        return jsonify(self.bl.put(uid, comment, annotatedSchema, humanReadableName))


