from configs.prod import ProductionConfig
from configs.prodDocker import ProductionConfigDocker
from configs.devMarcel import DevelopmentConfigMarcel
from configs.devAlex import DevelopmentConfigAlex
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.session import SparkSession
from configs.configHelper import hdfsIngestionURL, hdfsStorageURL, mongodbStorageURL, postgresStorageURL
from models.metaData import MetaData
import os

class SparkHelper():


  def __init__(self, appName):
    mapro_dev = os.environ.get("MAPRO_DEV")
    if mapro_dev == "alex":
      self.config = DevelopmentConfigAlex
    elif mapro_dev == "marcel":
      self.config = DevelopmentConfigMarcel
    elif mapro_dev == "robin":
      self.config = DevelopmentConfigMarcel
    else:
      if os.environ.get("IN_DOCKER", False):
        self.config = ProductionConfigDocker
      else:
        self.config = ProductionConfig

    try:
      self.sparkSession = SparkSession.builder \
        .master(self.config.SPARK_MASTER) \
        .appName(appName) \
        .config('spark.jars.packages',
          "org.mongodb.spark:mongo-spark-connector_2.12:3.0.0," +
          "org.postgresql:postgresql:42.2.18," +
          "com.databricks:spark-xml_2.12:0.10.0"
        ) \
        .getOrCreate()
    except Exception as err:
      print(err) 
      self.__raise("Failed to create SparkSession")

  
  def __raise(message, err: Exception):
    raise Exception(f"[SPARK_HELPER] {message}")


  #------------------------------------------------------------------------------------------------
  # MongoDB
  #------------------------------------------------------------------------------------------------

  # read from any mongodb source with optional authentication
  def readMongodb(
    self, host: str, port: int, user: str, password: str, database: str, collection: str
  ) -> DataFrame:
    auth = ""
    if user and password and (not user.isspace()) and (not password.isspace()):
      auth = f"{user}:{password}@"
    uri = f"mongodb://{auth}{host}:{port}/{database}?authSource=admin"
    try:
      return self.sparkSession.read \
        .format("com.mongodb.spark.sql.DefaultSource") \
        .option("spark.mongodb.input.uri", uri) \
        .option("collection", f"{collection}") \
        .load()
    except Exception as err:
      print(err)
      self.__raise(f"Failed to read from mongodb ({uri} - {collection})")

  
  # write to internal mongodb storage database
  def writeMongodb(self, dataframe: DataFrame, collection: str) -> str:
    try:
      # option for user and password instead of url
      dataframe.write \
        .format("com.mongodb.spark.sql.DefaultSource") \
        .option("spark.mongodb.output.uri", mongodbStorageURL(self.config)) \
        .option("collection", collection) \
        .mode("overwrite") \
        .save()
      return mongodbStorageURL(self.config)
    except Exception as err:
      print(err)
      self.__raise(f"Failed to write collection {collection} to internal MongoDB")


  #------------------------------------------------------------------------------------------------
  # PostgreSQL
  #------------------------------------------------------------------------------------------------

  # read from any postgresql
  def readPostrges(
    self, host: str, port: int, user: str, password: str, database: str, table: str
  ) -> DataFrame:
    uri=f"jdbc:postgresql://{host}:{port}/{database}"
    try:
      return self.sparkSession.read.jdbc(
        uri, 
        table=f'"{table}"',
        properties={
          "user": user,
          "password": password,
          "driver": "org.postgresql.Driver"
        }
      )
    except Exception as err:
      print(err)
      self.__raise(f"Failed to read from postgres ({uri} - {table})")


  # write to internal postgresql storage database
  def writePostgres(self, dataframe: DataFrame, table: str) -> str:
    try:
      dataframe.write.jdbc(
        postgresStorageURL(self.config),
        table=f'"{table}"',
        mode="overwrite",
        properties={
          "user": self.config.POSTGRES_USER,
          "password": self.config.POSTGRES_PASSWORD,
          "driver": "org.postgresql.Driver"
        }
      )
      return postgresStorageURL(self.config)
    except Exception as err:
      print(err)
      self.__raise(f"Failed to write table {table} to internal PostgreSQL")


  #------------------------------------------------------------------------------------------------
  # CSV
  #------------------------------------------------------------------------------------------------

  # read csv file from any hdfs
  def readCSV(
    self, namenode: str, port: int, filePath: str, hasHeader: str, delimiter: str
  ) -> DataFrame:
    uri=f"hdfs://{namenode}:{port}/{filePath}"
    try:
      return self.sparkSession.read.csv(uri, header=hasHeader, sep=delimiter, inferSchema=True)
    except Exception as err:
      print(err)
      self.__raise(f"Failed to read csv file from hdfs ({uri})")


  # read csv from ingestion dir
  def readCSVFromIngestion(self, jobId: str, hasHeader: bool, delimiter: str) -> DataFrame:
    try:
      return self.sparkSession.read.csv(
        f"{hdfsIngestionURL(self.config)}/{jobId}.csv",
        header=hasHeader,
        sep=delimiter,
        inferSchema=True
      )
    except Exception as err:
      print(err)
      self.__raise(f"Failed to read csv file {jobId}.csv from ingestion dir")


  # write as csv file to internal hdfs
  def writeCSV(self, dataframe: DataFrame, file: str, delimiter: str, hasHeader: bool) -> str:
    try:
      dataframe.write.csv(
        f"{hdfsStorageURL(self.config)}/csv/{file}",
        header=hasHeader,
        sep=delimiter,
        mode="overwrite"
      )
      return hdfsStorageURL(self.config) + "/csv"
    except Exception as err:
      print(err)
      self.__raise(f"Failed to write csv file {file} to internal Hdfs:")
  

  #------------------------------------------------------------------------------------------------
  # XML
  #------------------------------------------------------------------------------------------------

  # read xml file from any hdfs
  def readXML(self, namenode, port, filePath, rowTag) -> DataFrame:
    uri=f"hdfs://{namenode}:{port}/{filePath}"
    try:
      return self.sparkSession.read \
        .format("com.databricks.spark.xml") \
        .option("rowTag", rowTag) \
        .load(uri)
    except Exception as err:
      print(err)
      self.__raise(f"Failed to read xml file from hdfs ({uri})")


  # read xml file from ingestion dir
  def readXMLFromIngestion(self, jobId: str, rowTag: str) -> DataFrame:
    try:
      return self.sparkSession.read \
        .format("com.databricks.spark.xml") \
        .option("rowTag", rowTag) \
        .load(f"{hdfsIngestionURL(self.config)}/{jobId}.xml")
    except Exception as err:
      print(err)
      self.__raise(f"Failed to read xml file {jobId}.xml from ingestion dir")

  # write as xml file to internal hdfs
  def writeXML(self, dataframe: DataFrame, file: str, rowTag: str) -> str:
    try:
      dataframe.write \
        .format("com.databricks.spark.xml") \
        .option("rowTag", rowTag) \
        .mode("overwrite") \
        .save(f"{hdfsStorageURL(self.config)}/xml/{file}")
      return hdfsStorageURL(self.config) + "/xml"
    except Exception as err:
      print(err)
      self.__raise(f"Failed to write xml file {file} to internal hdfs")


  #------------------------------------------------------------------------------------------------
  # JSON
  #------------------------------------------------------------------------------------------------

  # read json file from any hdfs
  def readJSON(self, namenode, port, filePath) -> DataFrame:
    uri=f"hdfs://{namenode}:{port}/{filePath}"
    try:
      return self.sparkSession.read.json(uri, multiLine=True)
    except Exception as err:
      print(err)
      self.__raise(f"Failed to read json file from hdfs ({uri})")


  # read json file from ingestion dir
  def readJSONFromIngestion(self, jobId) -> DataFrame:
    try:
      return self.sparkSession.read.json(
        f"{hdfsIngestionURL(self.config)}/{jobId}.json",
        multiLine=True
      )
    except Exception as err:
      print(err)
      self.__raise(f"Failed to read json file {jobId}.json from ingestion dir")


  # write as json file to internal hdfs
  def writeJSON(self, dataframe: DataFrame, file:str) -> str:
    try:
      dataframe.write.json(f"{hdfsStorageURL(self.config)}/json/{file}", mode="overwrite")
      return hdfsStorageURL(self.config) + "/json"
    except Exception as err:
      print(err)
      self.__raise("Failed to write json file {file} to internal hdfs")


  #------------------------------------------------------------------------------------------------
  # Metadata
  #------------------------------------------------------------------------------------------------

  # read data from internal storage by metadata information
  def readFromMetadata(self, metadata: MetaData) -> DataFrame:
    try:
      if metadata.targetStorageSystem == "MongoDB":
        return self.sparkSession.read \
          .format("com.mongodb.spark.sql.DefaultSource") \
          .option("spark.mongodb.input.uri", mongodbStorageURL(self.config)) \
          .option("collection", metadata.uid) \
          .load()

      elif metadata.targetStorageSystem == "PostgreSQL":
        return self.sparkSession.read.jdbc(
          url=postgresStorageURL(self.config),
          table=f'"{metadata.uid}"',
          properties={
            "user": self.config.POSTGRES_USER,
            "password": self.config.POSTGRES_PASSWORD,
            "driver": "org.postgresql.Driver"
          }
        )

      elif metadata.targetStorageSystem == "HDFS":
        if metadata.mimetype == "text/csv":
          return self.sparkSession.read.csv(
            f"{hdfsStorageURL(self.config)}/csv/{metadata.uid}.csv",
            header=metadata.csvHasHeader,
            sep=metadata.csvDelimiter,
            inferSchema=True
          )

        elif metadata.mimetype == "application/xml":
          return self.sparkSession.read \
            .format("com.databricks.spark.xml") \
            .option("rowTag", metadata.xmlRowTag) \
            .load(f"{hdfsStorageURL(self.config)}/xml/{metadata.uid}.xml")

        elif metadata.mimetype == "application/json":
          return self.sparkSession.read.json(
            f"{hdfsStorageURL(self.config)}/json/{metadata.uid}.json"
          )

        else:
          self.__raise(f"Invalid mimetype {metadata.mimetype} in metadata {metadata.uid}")

      else:
        self.__raise(f"Read from metadata from, unknow tragetURL: {metadata.targetURL}")

    except Exception as err:
      print(err)
      self.__raise(f"Failed to read by metadata")
