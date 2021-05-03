#coding: utf-8
from datetime import datetime
from typing import List

from pkg_resources import require
from pyspark.sql.column import Column
from db.metaData import MetaDataDatabase
from apscheduler.schedulers.background import BackgroundScheduler
from flask_api import status
from models.user import User
from models.metaData import Ancestor, MetaData
import uuid
from spark import SparkHelper
from flask_restful import Resource
from flask_restful.reqparse import Argument
from services.decorators import parseParams
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify
from pyspark.sql import functions as F


STATE_RUNNING = 1
STATE_FINISHED  = 2
STATE_FAILED = 3
sessionStates = {}
metadataDb = MetaDataDatabase()

class SessionStore():
  def __init__(self):
    self.state: int = 0
    self.error: str = ""
    self.constructionCode: str = ""
    self.constructionQuery: str = ""


#--------------------------------------------------------------------------------------------------
# session api
#--------------------------------------------------------------------------------------------------
class DatamartSessionApi(Resource):
  @jwt_required
  def get(self):
    return f"datamart-{str(uuid.uuid4())}"


#--------------------------------------------------------------------------------------------------
# preview api
#--------------------------------------------------------------------------------------------------
class DatamartPreviewApi(Resource):
  def __generatePreview(self, session, datamarts, pyspark, query):
    sessionState: SessionStore = sessionStates[session]
    try:
      sparkHelper= SparkHelper(session)

      # laod all dataframes
      for identifier, metadataId in datamarts.items():
        metadata = metadataDb.get(metadataId)
        exec(f"{identifier} = sparkHelper.readFromMetadata(metadata)")

      exec(pyspark)

      for identifier, metadataId in datamarts.items():
        exec("{0}.createOrReplaceTempView('{0}')".format(identifier))

      dataframe = sparkHelper.sparkSession.sql(query)
      dataframe.createOrReplaceTempView("result")
      sessionState.constructionCode = pyspark
      sessionState.constructionQuery = query
      sessionState.state = STATE_FINISHED
    except Exception as err:
      sessionState.error = err
      sessionState.state = STATE_FAILED
      

  
  @jwt_required
  @parseParams(
    Argument("session", type=str, required=True),
    Argument("previewRowCount", type=int, default=10),
  )
  def get(self, session: str, previewRowCount: int):
    sessionState: SessionStore = sessionStates[session]
    # still generating preview
    if sessionState.state == STATE_RUNNING:
      return f"generating preview at session {session}", status.HTTP_202_ACCEPTED

    elif sessionState.state == STATE_FAILED:
      response: dict = {
        "message": f"generating preview failed:\n{sessionState.error}"
      }
      return response, status.HTTP_400_BAD_REQUEST

    # preview generated
    elif sessionState.state == STATE_FINISHED:
      sparkHelper = SparkHelper(session)
      dataframe = sparkHelper.sparkSession.sql("SELECT * FROM result")
      response: dict = {
        "schema": dataframe.schema.jsonValue(),
        "rows": dataframe.head(previewRowCount)
      }
      return response, status.HTTP_201_CREATED


  @jwt_required
  @parseParams(
    Argument("session", type=str, required=True),
    Argument("datamarts", type=dict, required=True),
    Argument("pyspark", type=str),
    Argument("query", type=str, required=True ),
  )
  def post(self, session, datamarts, pyspark, query):
    sessionStates[session] = SessionStore()
    sessionState: SessionStore = sessionStates[session]
    if sessionState.state == STATE_RUNNING:
      return f"generating preview at session {session}", status.HTTP_202_ACCEPTED

    else:
      scheduler = BackgroundScheduler()
      scheduler.add_job(lambda: self.__generatePreview(session, datamarts, pyspark, query))
      sessionState.state = STATE_RUNNING
      scheduler.start()
      return f"generating preview for session {session}", status.HTTP_200_OK
    

#--------------------------------------------------------------------------------------------------
# save api
#--------------------------------------------------------------------------------------------------
class DatamartSaveApi(Resource):
  @jwt_required
  @parseParams(
    Argument("session", type=str, required=True),
    Argument("datamarts", required=True, action="append"),
    Argument("humanReadableName", type=str, required=True),
    Argument("comment", type=str),
    Argument("targetStorageSystem", type=str),
    Argument("xmlRowTag", type=str),
    Argument("csvDelimiter", type=str),
    Argument("csvHasHeader", type=bool),
  )
  def post(
    self, datamarts, session, humanReadableName, comment, targetStorageSystem, xmlRowTag, 
    csvDelimiter, csvHasHeader
  ):
    sessionState: SessionStore = sessionStates[session]
    if sessionState.state == STATE_RUNNING:
      return f"generating preview at session {session}", status.HTTP_405_METHOD_NOT_ALLOWED

    sparkHelper = SparkHelper(session)
    dataframe = sparkHelper.sparkSession.sql("SELECT * FROM result")

    heritage = []
    for uid in datamarts:
      metadata: MetaData = metadataDb.get(uid)
      ancestor = Ancestor(
        uid=str(metadata.uid),
        heritage=metadata.heritage
      )
      heritage.append(ancestor)

    apiUser = User.objects(email__exact=get_jwt_identity()["email"]).get()

    targetURL = ""
    mimetype = ""
    isDatabase = False
    filename = ""
    uid = str(uuid.uuid4())
    if targetStorageSystem == 'MongoDB':
      isDatabase = True
      targetURL = sparkHelper.writeMongodb(dataframe, uid)
    elif targetStorageSystem == 'PostgreSQL':
      isDatabase = True
      targetURL = sparkHelper.writePostgres(dataframe, uid)
    elif targetStorageSystem == 'CSV':
      mimetype = "text/csv"
      filename = uid + ".csv"
      targetURL = sparkHelper.writeCSV(dataframe, filename, csvDelimiter, csvHasHeader)
    elif targetStorageSystem == 'XML':
      mimetype = "application/xml"
      filename = uid + ".xml"
      targetURL = sparkHelper.writeXML(dataframe, filename, xmlRowTag)
    elif targetStorageSystem == 'JSON':
      mimetype = "application/json"
      filename = uid + ".json"
      targetURL = sparkHelper.writeJSON(dataframe, filename)

    targetURL = sparkHelper.writeMongodb(dataframe, uid)

    metadata = MetaData(
      comment=comment,
      heritage=heritage,
      humanReadableName=humanReadableName,
      insertedAt=datetime.now(),
      insertedBy=apiUser,
      isDatabase=isDatabase,
      schema=dataframe.schema.json(),
      targetStorageSystem="MongoDB",
      targetURL=targetURL,
      uid=uid,
      csvDelimiter=csvDelimiter,
      csvHasHeader=csvHasHeader,
      mimetype=mimetype,
      filename=filename,
      xmlRowTag=xmlRowTag,
      constructionCode=sessionState.constructionCode,
      constructionQuery=sessionState.constructionQuery
    )
    metadata.save()

    sparkHelper.sparkSession.stop()
    return uid