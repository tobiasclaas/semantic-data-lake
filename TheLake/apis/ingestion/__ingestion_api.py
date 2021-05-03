import datetime
import enum
import os
from spark import SparkHelper
from mongoengine.fields import BooleanField

from pyspark.sql.dataframe import DataFrame
from models.metaData import MetaData
import uuid
from models.job import Job
from pyspark.sql import SparkSession, functions
from server import server as app

class SourceTypes(enum.Enum):
  MONGO = 1
  POSTGRES = 2
  JSON = 3
  XML = 4
  CSV = 5
    

def create_job(job_id, task, api_user) -> Job:
  try:
    job: Job = Job(
      uid=job_id,
      task=task,
      errorMessage='',
      startedBy=api_user,
      startedAt=datetime.datetime.now(),
      failed=False
    )
    job.save()
    return job
  except Exception as err: raise Exception(f"[JOB] failed to create: {err}")


def job_succeeded(job: Job) -> Job:
  job.failed = False
  job.endedAt = datetime.datetime.now()
  job.save()
  return job


def job_failed(exception, job: Job) -> Job:
  if job is not None:
    job.failed = True
    job.errorMessage = str(exception)
    job.endedAt = datetime.datetime.now()
    job.save()  
    return job 


def write_to_datalake(
  dataframe: DataFrame, sparkHelper: SparkHelper, srcType: SourceTypes, targetStorage: str,
  csvDelimiter=",", csvHasHeader=False, xmlRowTag: str = ''
) -> tuple[str, str, uuid.UUID]:
  with app.app_context():
    targetUrl = ""
    mimeType = ""
    uid = uuid.uuid4()

    try:
      if targetStorage == "MongoDB":
          targetUrl = sparkHelper.writeMongodb(dataframe, f"{uid}")

      elif targetStorage == "PostgreSQL":
        if srcType == SourceTypes.CSV or srcType == SourceTypes.XML or srcType == SourceTypes.JSON:
          raise Exception("[INGESTION] unsupported operation saving file to PostgreSQL")
        elif srcType == SourceTypes.MONGO:
          flatCols = [c[0] for c in dataframe.dtypes if c[1][:6] != 'struct']
          nestedCols = [c[0] for c in dataframe.dtypes if c[1][:6] == 'struct']
          flattened_dataframe = dataframe.select(
            flatCols + [
              functions.col(nc + '.' + c).alias(nc + '_' + c)
              for nc in nestedCols
              for c in dataframe.select(nc + '.*').columns
            ]
          )
          dataframe = flattened_dataframe
        targetUrl = sparkHelper.writePostgres(dataframe, f"{uid}")
      
      elif targetStorage == "HDFS":
        if srcType == SourceTypes.CSV:
          mimeType = "text/csv"
          targetUrl = sparkHelper.writeCSV(dataframe, f"{uid}.csv", csvDelimiter, csvHasHeader)
          
        elif srcType == SourceTypes.XML:
          mimeType = "application/xml"
          targetUrl = sparkHelper.writeXML(dataframe, f"{uid}.xml", xmlRowTag)

        else:
          mimeType = "application/json"
          targetUrl = sparkHelper.writeJSON(dataframe, f"{uid}.json")

      else:
        raise Exception(f"Invalid target system: {targetStorage}")
                
    except Exception as err: raise Exception(f"[DATALAKE] failed to write {err}")

    return targetUrl, mimeType, uid


def save_db_metadata(
  uid, dataframe, src_connection, src_db_user, src_db_password, src_database, src_collection, 
  mime_type, comment, api_user, target_storgae, target_url, humanReadableName, meta_data
) -> MetaData:
  try:
    metaData = MetaData(
      uid=uid,
      sourceConnection=src_connection,
      sourceUser=src_db_user,
      sourcePassword=src_db_password,
      sourceDBName=src_database,
      sourceCollectionOrTableName=src_collection,
      isDatabase=True,
      mimetype=mime_type,
      schema=dataframe.schema.json(),
      insertedAt=datetime.datetime.now(),
      comment=comment,
      insertedBy=api_user,
      targetStorageSystem=target_storgae,
      targetURL=target_url,
      humanReadableName=humanReadableName
    )
    meta_data.objects.insert(metaData)
    return meta_data
  except Exception as err: raise Exception(f"[METADATA] failed to create: {err}")

def save_file_metadata(
  uid, dataframe, file, csv_delimiter, csv_has_header, mime_type, comment, api_user, 
  target_storgae, target_url, humanReadableName, meta_data, rowTag
) -> MetaData:
  try:
    metaData = MetaData(
      uid=uid,
      mimetype = file.mimetype,
      schema=dataframe.schema.json(),
      insertedAt=datetime.datetime.now(),
      comment = comment,
      insertedBy = api_user,
      targetStorageSystem = target_storgae,
      targetURL = target_url,
      csvDelimiter = csv_delimiter,
      filename=file.filename,
      csvHasHeader = csv_has_header,
      humanReadableName = humanReadableName,
      xmlRowTag=rowTag
    )
    meta_data.objects.insert(metaData)
    return meta_data
  except Exception as err: raise Exception(f"[METADATA] failed to create: {err}")