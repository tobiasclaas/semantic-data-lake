import json
import datetime
from flask import request
from flask_restful import Resource
from pyspark.sql.types import *
from pyspark.sql.functions import *

from database.data_access import datamart_data_access as data_access
from Utils.spark import SparkHelper

from Utils.services.create_datamart import create_datamart
from Utils.ingestion import ingest_spark_helper
from database.models import CsvStorage, DatamartState
from apscheduler.schedulers.background import BackgroundScheduler

source_ids = []


def flatten(df):
    """
    This functions is given by: https://gist.github.com/nmukerje/e65cde41be85470e4b8dfd9a2d6aed50
    Flattens a complex json/xml dataframe to tabular data
    :param df: pyspark dataframe object
    :return: pyspark dataframe object
    """
    # compute Complex Fields (Lists and Structs) in Schema
    complex_fields = dict([(field.name, field.dataType)
                           for field in df.schema.fields
                           if type(field.dataType) == ArrayType or  type(field.dataType) == StructType])
    while len(complex_fields)!=0:
        col_name=list(complex_fields.keys())[0]
        print ("Processing :"+col_name+" Type : "+str(type(complex_fields[col_name])))

        # if StructType then convert all sub element to columns.
        # i.e. flatten structs
        if (type(complex_fields[col_name]) == StructType):
            expanded = [col(col_name+'.'+k).alias(col_name+'_'+k) for k in [ n.name for n in  complex_fields[col_name]]]
            df=df.select("*", *expanded).drop(col_name)

        # if ArrayType then add the Array Elements as Rows using the explode function
        # i.e. explode Arrays
        elif (type(complex_fields[col_name]) == ArrayType):
            df=df.withColumn(col_name,explode_outer(col_name))

        # recompute remaining Complex Fields in Schema
        complex_fields = dict([(field.name, field.dataType)
                               for field in df.schema.fields
                               if type(field.dataType) == ArrayType or  type(field.dataType) == StructType])
    return df


def process_input(spark_helper, data):
    """
    Processes the data['input'] field recursively. Base condition is data['type'] == 'data_source' 
    where a datamart is read from source and returns a pyspark Dataframe object.
    :param spark_helper: To re-use single spark session object.
    :param data: Dictionary object containing 'input' and 'type' mandatory keys and other keys
    based on 'type.
    :return: Dataframe. A pyspark Dataframe object.
    """
    if data['type'] == 'join':
        df1 = process_input(spark_helper, data['input'][0]['input'][0])
        df2 = process_input(spark_helper, data['input'][1]['input'][0])
        if data['input'][0]['column'] == data['input'][1]['column']:
            return df1.join(df2, data['input'][0]['column'])
        else:
            return df1.join(df2, df1[data['input'][0]['column']] == df2[data['input'][1]['column']])

    elif data['type'] == 'filter':
        df1 = process_input(spark_helper, data['input'][0])
        return df1.filter(data["condition"])

    elif data['type'] == 'select':
        df1 = process_input(spark_helper, data['input'][0])
        if 'distinct' in data.keys() and data['distinct']:
            return df1.select(*data["columns"]).distinct()
        return df1.select(*data["columns"])

    elif data['type'] == 'groupby':
        df1 = process_input(spark_helper, data['input'][0])
        return df1.groupBy(*data['column']).agg(data["aggregate"])

    elif data['type'] == 'flatten':
        df1 = process_input(spark_helper, data['input'][0])
        return flatten(df1)

    elif data['type'] == 'data_source':
        source_ids.append(data['uid'])
        datamart = data_access.get_by_uid(data['uid'])
        return spark_helper.read_datamart(datamart)


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

    def post(self, workspace_id):
        """
        Data is fetched using request.data method. Data is a array of json(dictionary) objects.
        It just submits the request and doesn't return anything. To check if request was
        completed successfully, check if the target datamart is showing in Data management tab.
        """
        spark_helper = SparkHelper("transform")
        try:
            data = json.loads(request.data)
            for data_input in data:
                human_readable_name = data_input["name"]

                # data_input['input'] is always an array of dictionary objects. though only index [0]
                # is fetched everytime except for case of join, where 2 inputs are required
                transformed_dataframe = process_input(spark_helper, data_input['input'][0])

                source = CsvStorage(
                    file=f"{','.join(source_ids)}",
                    has_header = True
                )

                # data_input['target'] is just a string with possible values: 'HDFS', 'MongoDB', 'Postgres'
                __start__(spark_helper, transformed_dataframe, None, source, data_input['target'], workspace_id,
                          human_readable_name, "")

        except Exception as e:
            if (spark_helper):
                spark_helper.spark_session.stop()

            print(e)
