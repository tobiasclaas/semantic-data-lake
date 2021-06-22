import datetime
import uuid

from apscheduler.schedulers.background import BackgroundScheduler
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from flask_restful.reqparse import Argument
from pywebhdfs.webhdfs import PyWebHdfsClient
from werkzeug.datastructures import FileStorage

import settings
from api.services.decorators import parse_params
from business_logic.services.create_datamart import create_datamart
from business_logic.services.mapper import mapper
from business_logic.ingestion import ingest

from database.data_access import user_data_access
from database.models import (
    MongodbStorage, PostgresqlStorage, DatamartState, CsvStorage, JsonStorage, XmlStorage
)


def __start__(api_user, source, target_storage, workspace_id, hnr, comment):
    datamart = create_datamart(api_user, source, target_storage, workspace_id, hnr, comment)

    try:
        scheduler = BackgroundScheduler()

        datamart.status.started = datetime.datetime.now()
        datamart.status.state = DatamartState.RUNNING
        datamart.save()

        scheduler.add_job(
            lambda: ingest(datamart)
        )
        scheduler.start()

        return datamart
    except Exception as e:
        datamart.status.state = DatamartState.FAILED
        datamart.status.error = f"{e}"
        datamart.status.ended = datetime.datetime.now()
        return e


class MongodbIngestion(Resource):
    @jwt_required
    @parse_params(
        Argument("host", default='', type=str, required=True),
        Argument("port", default='', type=str, required=True),
        Argument("database", default='', type=str, required=True),
        Argument("collection", default='', type=str, required=True),
        Argument("target_storage", default='MongoDB', type=str, required=False),
        Argument("user", default='', type=str, required=False),
        Argument("password", default='', type=str, required=False),
        Argument("comment", default='', type=str, required=False),
        Argument("human_readable_name", default='', type=str, required=False)
    )
    def post(
            self, host, port, database, collection, workspace_id, target_storage, user, password, comment,
            human_readable_name
    ):
        api_user = user_data_access.get_by_email(get_jwt_identity()["email"])

        source = MongodbStorage(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            collection=collection
        )

        return jsonify(
            mapper(__start__(api_user, source, target_storage, workspace_id, human_readable_name, comment))
        )


class PostgresqlIngestion(Resource):
    @jwt_required
    @parse_params(
        Argument("host", default='', type=str, required=True),
        Argument("port", default='', type=str, required=True),
        Argument("database", default='', type=str, required=True),
        Argument("table", default='', type=str, required=True),
        Argument("target_storage", default='PostgreSQL', type=str, required=False),
        Argument("user", default='', type=str, required=False),
        Argument("password", default='', type=str, required=False),
        Argument("comment", default='', type=str, required=False),
        Argument("human_readable_name", default='', type=str, required=False)
    )
    def post(
            self, host, port, database, table, workspace_id, target_storage, user, password, comment,
            human_readable_name
    ):
        api_user = user_data_access.get_by_email(get_jwt_identity()["email"])

        source = PostgresqlStorage(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            table=table
        )

        return jsonify(
            mapper(__start__(api_user, source, target_storage, workspace_id, human_readable_name, comment))
        )


class CsvIngestion(Resource):
    @jwt_required
    @parse_params(
        Argument("file", type=FileStorage, location='files', required=True),
        Argument("delimiter", default=';', type=str, required=False),
        Argument("has_header", default=False, type=bool, required=False),
        Argument("target_storage", default='HDFS', type=str, required=False),
        Argument("comment", default='', type=str, required=False),
        Argument("human_readable_name", default='', type=str, required=False),
    )
    def post(
            self, workspace_id, file: FileStorage, delimiter, has_header, target_storage, comment,
            human_readable_name
    ):
        api_user = user_data_access.get_by_email(get_jwt_identity()["email"])
        hdfs = settings.Settings().hdfs_storage

        source = CsvStorage(
            file=f"{hdfs.ingestion_directory}/{workspace_id}/{uuid.uuid4()}.csv",
            has_header=has_header,
            delimiter=delimiter
        )

        client = PyWebHdfsClient(host=hdfs.namenode, port="9870")
        client.create_file(source.file, file)

        return jsonify(
            mapper(__start__(api_user, source, target_storage, workspace_id, human_readable_name, comment))
        )


class JsonIngestion(Resource):
    @jwt_required
    @parse_params(
        Argument("file", type=FileStorage, location='files', required=True),
        Argument("target_storage", default='HDFS', type=str, required=False),
        Argument("comment", default='', type=str, required=False),
        Argument("human_readable_name", default='', type=str, required=False),
    )
    def post(
            self, workspace_id, file: FileStorage, target_storage, comment,
            human_readable_name
    ):
        api_user = user_data_access.get_by_email(get_jwt_identity()["email"])
        hdfs = settings.Settings().hdfs_storage

        source = JsonStorage(
            file=f"{hdfs.ingestion_directory}/{workspace_id}/{uuid.uuid4()}.json"
        )

        client = PyWebHdfsClient(host=hdfs.namenode, port="9870")
        client.create_file(source.file, file)

        return jsonify(
            mapper(__start__(api_user, source, target_storage, workspace_id, human_readable_name, comment))
        )


class XmlIngestion(Resource):
    @jwt_required
    @parse_params(
        Argument("file", type=FileStorage, location='files', required=True),
        Argument("row_tag", default=';', type=str, required=False),
        Argument("target_storage", default='HDFS', type=str, required=False),
        Argument("comment", default='', type=str, required=False),
        Argument("human_readable_name", default='', type=str, required=False),
    )
    def post(
            self, workspace_id, file: FileStorage, row_tag, target_storage, comment,
            human_readable_name
    ):
        api_user = user_data_access.get_by_email(get_jwt_identity()["email"])
        hdfs = settings.Settings().hdfs_storage

        source = XmlStorage(
            file=f"{hdfs.ingestion_directory}/{workspace_id}/{uuid.uuid4()}.xml",
            row_tag=row_tag,
        )

        client = PyWebHdfsClient(host=hdfs.namenode, port="9870")
        client.create_file(source.file, file)

        return jsonify(
            mapper(__start__(api_user, source, target_storage, workspace_id, human_readable_name, comment))
        )
