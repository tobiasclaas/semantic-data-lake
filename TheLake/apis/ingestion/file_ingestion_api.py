from configs.configHelper import hdfsIngestionURL
from os import mkdir, path
from spark import SparkHelper
from flask_restful.inputs import boolean
from pyspark.sql.dataframe import DataFrame
from pywebhdfs import webhdfs
import werkzeug
from werkzeug.datastructures import FileStorage
from models.user import User
from flask import app, jsonify
from flask_restful import Resource
from pyspark.sql import SparkSession
from models.job import Job
from .__ingestion_api import *
from collections import UserDict
from models.metaData import MetaData
import uuid
from apscheduler.schedulers.background import BackgroundScheduler
from flask_jwt_extended.utils import get_jwt_identity
from models.job import Job
from flask_restful.reqparse import Argument
from services.decorators import parseParams
from flask_jwt_extended.view_decorators import jwt_required
from flask_restful import Resource
from pyspark.sql import SparkSession
from flask import jsonify
from server import server as app
import requests
from pywebhdfs.webhdfs import PyWebHdfsClient

class FileIngestion(Resource):

    file_extensions = {
        SourceTypes.JSON: "json",
        SourceTypes.XML: "xml",
        SourceTypes.CSV: "csv",
    }


    def __ingest(
        self, api_user: User, file: FileStorage, src_type: SourceTypes,
        delimiter: str, has_header: boolean, target_storage: str, comment: str, 
        humanReadableName: str, jobId: str, rowTag: str
    ):
        job: Job = None
        sparkHelper: SparkHelper = None

        try:
            task = f"Ingestion in data lake from file: {file.filename}"
            job = create_job(jobId, task, api_user)
            sparkHelper = SparkHelper(f"Ingestion {job.uid}")
            dataframe: DataFrame = None

            if src_type == SourceTypes.CSV:
                dataframe = sparkHelper.readCSVFromIngestion(job.uid, has_header, delimiter)

            elif src_type == SourceTypes.XML:
                dataframe = sparkHelper.readXMLFromIngestion(job.uid, rowTag)

            elif src_type == SourceTypes.JSON:
                dataframe = sparkHelper.readJSONFromIngestion(job.uid)
            
            else:
                raise Exception("[INGESTION] no valid source file type")
                
            dataframe.show()
            dataframe.printSchema()

            target_url, mime_type, uid = write_to_datalake(
                dataframe, sparkHelper, src_type, target_storage, delimiter, has_header, rowTag
            )

            save_file_metadata(
                uid, dataframe, file, delimiter, has_header, mime_type, comment, 
                api_user, target_storage, target_url, humanReadableName, MetaData, rowTag
            )

            job_succeeded(job)
        
        except Exception as err:
            job_failed(err, job)

        finally:
            if sparkHelper is not None:
                sparkHelper.sparkSession.stop()
                    

    @jwt_required
    @parseParams(
        Argument("file", type=werkzeug.datastructures.FileStorage, location='files', required=True), 
        Argument("delimiter", default=';', type=str, required=False), 
        Argument("hasHeader", default=False, type=boolean, required=False),
        Argument("targetStorageSystem", default='HDFS', type=str, required=False),
        Argument("comment", default='', type=str, required=False), 
        Argument("humanReadableName", default='', type=str, required=False),
        Argument("rowTag", type=str, default="Match", required=False)
    )
    def post(
        self, file: FileStorage, delimiter, hasHeader, targetStorageSystem, comment, 
        humanReadableName, rowTag
    ):
        scheduler = BackgroundScheduler()
        apiUser = User.objects(email__exact=get_jwt_identity()["email"]).get()
        jobId = uuid.uuid4()

        srcType: SourceTypes
        if file.mimetype == "text/csv":
            tmp_file = str(jobId) + ".csv"
            srcType = SourceTypes.CSV

        elif file.mimetype == "application/xml":
            tmp_file = str(jobId) + ".xml"
            srcType = SourceTypes.XML

        elif file.mimetype == "application/json":
            tmp_file = str(jobId) + ".json"
            srcType = SourceTypes.JSON
        else:
            return jsonify({"message": "{} not supported".format(file.mimetype)})

        with app.app_context():
            hdfsClient = PyWebHdfsClient(host="namenode", port="9870")
            hdfsClient.create_file(f"{app.config['HDFS_INGESTION_DIR']}/{tmp_file}", file)

        scheduler.add_job( 
            lambda: self.__ingest(
                apiUser, file, srcType, delimiter, hasHeader, targetStorageSystem,
                comment, humanReadableName, jobId, rowTag
            ),
        )
        scheduler.start()
        return jsonify({"jobID": jobId, "status": "started"})