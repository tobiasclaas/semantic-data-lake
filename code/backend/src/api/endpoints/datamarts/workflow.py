import json
import uuid
import datetime
from flask import jsonify, Response, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from flask_restful.reqparse import Argument
from api.services.decorators import parse_params
from business_logic.services.mapper import mapper
from database.data_access import datamart_data_access as data_access, user_data_access
from business_logic.spark import SparkHelper
import settings

from werkzeug.datastructures import FileStorage
from business_logic.services.create_datamart import create_datamart
from business_logic.ingestion import ingest_spark_helper
from business_logic.services.mapper import mapper
from database.models import User, Datamart, Metadata, MongodbStorage, PostgresqlStorage, CsvStorage, \
    XmlStorage, JsonStorage, DatamartStatus, DatamartState
from apscheduler.schedulers.background import BackgroundScheduler

source_ids = []


def process_input(spark_helper, data):
    """ input will be a json, return a datamart"""
    if data['type'] == 'join':
        df1 = process_input(spark_helper, data['input'][0]['input'][0])
        df2 = process_input(spark_helper, data['input'][1]['input'][0])
        if data['input'][0]['column'] == data['input'][1]['column']:
            dataframe = df1.join(df2, data['input'][0]['column'])
        else:
            dataframe = df1.join(df2, df1[data['input'][0]['column']] == df2[data['input'][1]['column']])
        return dataframe

    if data['type'] == 'filter':
        df1 = process_input(spark_helper, data['input'][0])
        dataframe = df1.filter(data["condition"])
        return dataframe

    if data['type'] == 'select':
        df1 = process_input(spark_helper, data['input'][0])
        dataframe = df1.select(*data["columns"])
        return dataframe

    if data['type'] == 'data_source':
        source_ids.append(data['uid'])
        datamart = data_access.get_by_uid(data['uid'])
        dataframe = spark_helper.read_datamart(datamart)
        return dataframe


def __start__(spark_helper, dataframe, api_user, source, target_storage, workspace_id, hnr, comment):
    datamart = create_datamart(api_user, source, target_storage, workspace_id, hnr, comment)

    try:
        scheduler = BackgroundScheduler()

        datamart.status.started = datetime.datetime.now()
        datamart.status.state = DatamartState.RUNNING
        datamart.save()

        scheduler.add_job(
            lambda: ingest_spark_helper(datamart, spark_helper, dataframe)
        )
        scheduler.start()

        return datamart
    except Exception as e:
        datamart.status.state = DatamartState.FAILED
        datamart.status.error = f"{e}"
        datamart.status.ended = datetime.datetime.now()
        return e


class WorkFlow(Resource):

    @parse_params(
        # Argument("file", type=FileStorage, location='files', required=True)
        # Argument("workflow", type=str, required=False)
    )
    def post(self, workspace_id):

        spark_helper = SparkHelper("transform")
        try:


            data = json.loads(request.data)
            for data_input in data:
                human_readable_name = data_input["name"]
                transformed_dataframe = process_input(spark_helper, data_input['input'][0])
                # transformed_dataframe.show()

                source = CsvStorage(
                    file=f"{','.join(source_ids)}",
                    has_header=True
                )
                __start__(spark_helper, transformed_dataframe, None, source, data_input['target'], workspace_id,
                          human_readable_name, "")
                # target = CsvStorage(
                #     file=f"{hdfs.ingestion_directory}/{workspace_id}/transform_{uuid.uuid4()}.csv",
                # )

            return Response(status=200)

        except Exception as e:
            if (spark_helper):
                spark_helper.spark_session.stop()

            print(e)
