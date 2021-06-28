import json
import uuid
import datetime
from flask import jsonify, Response
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from flask_restful.reqparse import Argument
from api.services.decorators import parse_params
from business_logic.services.mapper import mapper
from database.data_access import datamart_data_access as data_access, user_data_access
from business_logic.spark import SparkHelper
import settings

from werkzeug.datastructures import FileStorage
from business_logic.services.create_datamart import create_datamart_workflow
from business_logic.ingestion import ingest_spark_helper
from business_logic.services.mapper import mapper
from database.models import User, Datamart, Metadata, MongodbStorage, PostgresqlStorage, CsvStorage, \
    XmlStorage, JsonStorage, DatamartStatus, DatamartState
from apscheduler.schedulers.background import BackgroundScheduler

def process_input(spark_helper, data):
    """ input will be a json, return a datamart"""
    if "type" in data.keys() and data['type'] == 'join':
        df1 = process_input(spark_helper, data['input'][0]['input'][0])
        df2 = process_input(spark_helper, data['input'][1]['input'][0])
        if data['input'][0]['column'] == data['input'][1]['column']:
            dataframe = df1.join(df2, data['input'][0]['column'])
        else:
            dataframe = df1.join(df2, df1[data['input'][0]['column']] == df2[data['input'][1]['column']])
        return dataframe

    if "type" in data.keys() and data['type'] == 'filter':
        df1 = process_input(spark_helper, data['input'][0])
        dataframe = df1.filter(data["condition"])
        # Still need to write this functionalaiy
        return dataframe

    if "type" in data.keys() and data['type'] == 'select':
        df1 = process_input(spark_helper, data['input'][0])
        dataframe = df1.select(*data["columns"])
        return dataframe

    if "type" in data.keys() and data['type'] == 'source':
        datamart = data_access.get_by_uid(data['id'])
        dataframe = spark_helper.read_datamart(datamart)
        return dataframe


def __start__(spark_helper, dataframe, api_user, source, target_storage, workspace_id, hnr, comment):
    datamart = create_datamart_workflow(api_user, source, target_storage, workspace_id, hnr, comment)

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

    @jwt_required
    @parse_params(
        #Argument("file", type=FileStorage, location='files', required=True)
        Argument("workflow", type=str, required=True)
    )
    def post(self, workspace_id, workflow):
        
        spark_helper = SparkHelper("transform")
        setting = settings.Settings()
        try:
            file = r"""{
                           "type":"output",
                           "name":"exported.csv",
                           "target":"HDFS",
                           "input":[
                              {
                                 "type":"filter",
                                 "condition":"Identifier= \"9012\" ",
                                 "input":[
                                    {
                                       "type":"select",
                                       "columns":[
                                          "Identifier",
                                          "Access code",
                                          "Recovery code",
                                          "First name2",
                                          "Last name2",
                                          "Department",
                                          "Location"
                                       ],
                                       "input":[
                                          {
                                             "type":"join",
                                             "input":[
                                                {
                                                   "column":"Identifier",
                                                   "input":[
                                                      {
                                                         "type":"source",
                                                         "id":"f9bd1508-b5d3-4b44-92a0-a8734c41f783"
                                                      }
                                                   ]
                                                },
                                                {
                                                   "column":"Identifier",
                                                   "input":[
                                                      {
                                                         "type":"source",
                                                         "id":"bb470ec0-36c3-44ad-932f-27250cad8f15"
                                                      }
                                                   ]
                                                }
                                             ]
                                          }
                                       ]
                                    }
                                 ]
                              }
                           ]
                        }"""
            api_user = user_data_access.get_by_email(get_jwt_identity()["email"])
            hdfs = settings.Settings().hdfs_storage
            data = json.loads(file)
            human_readable_name = data["name"]
            for data_input in data['input']:
                transformed_dataframe = process_input(spark_helper, data_input)
            
            source = CsvStorage(
                file=f"source ids",
            )
            target = CsvStorage(
                file=f"{hdfs.ingestion_directory}/{workspace_id}/transform_{uuid.uuid4()}.csv",
            )
            
            return jsonify(mapper(__start__(spark_helper, transformed_dataframe, api_user, source, target, workspace_id, human_readable_name, workflow)))

        except Exception as e:
            if (spark_helper):
                spark_helper.spark_session.stop()

            print(e)
