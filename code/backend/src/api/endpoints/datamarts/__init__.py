from flask import jsonify
import pymongo
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from flask_restful.reqparse import Argument
from pywebhdfs.webhdfs import PyWebHdfsClient

from business_logic.spark import SparkHelper
from database.models import (
    MongodbStorage, PostgresqlStorage,
    CsvStorage, JsonStorage, XmlStorage, Datamart
)
import settings
from api.services.decorators import parse_params
from business_logic.services.mapper import mapper
from database.data_access import datamart_data_access as data_access


def delete_from_hdfs(file_name):
    hdfs = settings.Settings().hdfs_storage
    client = PyWebHdfsClient(host=hdfs.namenode, port="9870")
    client.delete_file_dir(file_name, recursive=True)


def Delete_data(storage):
    if isinstance(storage, CsvStorage):
        # Checks if csv extension available in file name. Their is a special case
        # where CsvStorage object is created and file is not present in HDFS.
        # That is in Workflow Api
        if '.csv' in storage.file:
            delete_from_hdfs(storage.file)

    elif isinstance(storage, JsonStorage) or isinstance(storage, XmlStorage):
        delete_from_hdfs(storage.file)

    elif isinstance(storage, MongodbStorage):
        auth = f"{storage.user}:{storage.password}@"
        uri = f"mongodb://{auth}{storage.host}:{storage.port}/{storage.database}?authSource=admin"
        myclient = pymongo.MongoClient(uri)
        mydb = myclient[storage.database]
        mydb[storage.collection].drop()

    #
    # elif isinstance(storage, PostgresqlStorage):
    #     dataframe = spark_helper.read_postrgesql(source)



class Datamarts(Resource):

    @parse_params(
        Argument("page", default=1, type=int, required=False),
        Argument("limit", default=10, type=int, required=False),
        Argument("field_to_order", default="created_at", type=str, required=False),
        Argument("asc", default=False, type=bool, required=False),
        Argument("search", default=None, type=str, required=False),
        Argument("uid", default=None, type=str, required=False),
        Argument("data_only", default=False, type=str, required=False),
    )
    def get(self, workspace_id, uid, data_only, page, limit, field_to_order, asc, search):
        if uid is None:
            result = []
            datamarts = data_access.get_list(page, limit, field_to_order, asc, search)

            for datamart in datamarts.items:
                if mapper(datamart)['workspace_id'] == workspace_id:
                    result.append(mapper(datamart))

            return jsonify(result)
        else:
            datamart = data_access.get_by_uid(uid)
            if data_only:
                try:
                    spark_helper = SparkHelper("Read Data")
                    data = spark_helper.read_datamart(datamart).toPandas().to_json()
                    spark_helper.spark_session.stop()
                    return data
                except Exception as e:
                    if (spark_helper):
                        spark_helper.spark_session.stop()
                    print(e)

            return jsonify(mapper(datamart))

    @parse_params(
        Argument("uid", type=str, required=False),
    )
    def delete(self, workspace_id, uid):
        if uid is None:
            Datamart.objects.filter(workspace_id=workspace_id).delete()
            return "All datamarts deleted"

        datamart = data_access.get_by_uid(uid)
        if datamart.workspace_id == workspace_id:
            hnr = datamart.human_readable_name
            try:
                Delete_data(datamart.metadata.source)
                Delete_data(datamart.metadata.target)
            except Exception as e:
                print (e)

            datamart.delete()
            return f"deleted datamart {hnr}"
        else:
            return "Permission not allowed"

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
        datamart.metadata.schema = annotated_schema \
            .replace("\'", "\"") \
            .replace(" ", "") \
            .replace("True", "true") \
            .replace("False", "false")
        datamart.save()
        return jsonify(mapper(datamart))
