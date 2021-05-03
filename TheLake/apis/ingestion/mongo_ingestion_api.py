from spark import SparkHelper
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

class MongoIngestion(Resource):
    def ingest(
        self, apiUser, host, port, database, collection, dbUser, dbPassword, targetStorage, 
        comment, humanReadableName, jobId
    ):
        with app.app_context():
            sparkHelper: SparkHelper = None
            job: Job = None

            try:
                task = f"Ingestion in data lake of {database}.{collection} from: {host}:{port}"
                job = create_job(jobId, task, apiUser)
                sparkHelper = SparkHelper(job)

                dataframe = sparkHelper.readMongodb(
                    host, port, dbUser, dbPassword, database, collection
                ) 
                
                dataframe.show()
                dataframe.printSchema()
                
                target_url, mime_type, uid = write_to_datalake(
                    dataframe, sparkHelper, SourceTypes.MONGO, targetStorage
                )
                save_db_metadata(
                    uid, dataframe, f"{host}:{port}/{database}", dbUser, dbPassword, database, 
                    collection, mime_type, comment, apiUser, targetStorage, target_url,
                    humanReadableName, MetaData
                )
                job_succeeded(job)

            except Exception as err: 
                job_failed(err, job)

            finally:
                if sparkHelper is not None:
                    sparkHelper.sparkSession.stop()
        


    @jwt_required
    @parseParams(
        Argument("host", default='', type=str, required=True),
        Argument("port", default='', type=str, required=True),
        Argument("database", default='', type=str, required=True),
        Argument("collection", default='', type=str, required=True),
        Argument("targetStorageSystem", default='MongoDB', type=str, required=False),
        Argument("user", default='', type=str, required=False),
        Argument("password", default='', type=str, required=False),
        Argument("comment", default='', type=str, required=False),
        Argument("humanReadableName", default='', type=str, required=False)
    )
    def post(
        self, host, port, database, collection, targetStorageSystem, user, password, comment,
        humanReadableName
    ):
        scheduler = BackgroundScheduler()
        apiUser = User.objects(email__exact=get_jwt_identity()["email"]).get()
        jobId = uuid.uuid4()
        scheduler.add_job(
            lambda: self.ingest(
                apiUser, host, port, database, collection, user, password, targetStorageSystem, 
                comment, humanReadableName, jobId
            )
        )    
        scheduler.start()
        return jsonify({"jobID": jobId, "status": "started"})  