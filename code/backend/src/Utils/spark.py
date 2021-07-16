
from pyspark import SparkContext, SparkConf
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.session import SparkSession

from database.models import (
    MongodbStorage, PostgresqlStorage, CsvStorage, JsonStorage, XmlStorage,
    Datamart
)
from settings import Settings


class SparkHelper:
    def __init__(self, app_name):
        self.settings = Settings()
        try:
            conf = SparkConf().set("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:3.0.0," +
                                                          "org.postgresql:postgresql:42.2.18," +
                                                          "com.databricks:spark-xml_2.12:0.10.0")
            SparkContext(master="local", conf=conf) # For fixing "Failed to create pysparkSession" error        
            self.spark_session = SparkSession.builder \
                .master(self.settings.spark_master) \
                .appName(app_name) \
                .getOrCreate() \
                
        except Exception as err:
            print(err)
            self.__raise("Failed to create SparkSession")

    def __raise(self, message):
        raise Exception(f"[SPARK_HELPER] {message}")

    # ==============================================================================================
    # MongoDB
    # ==============================================================================================

    # read from any mongodb source with optional authentication
    def read_mongodb(self, storage: MongodbStorage) -> DataFrame:
        auth = ""
        user = storage.user
        password = storage.password

        if user and password and (not user.isspace()) and (not password.isspace()):
            auth = f"{user}:{password}@"

        uri = f"mongodb://{auth}{storage.host}:{storage.port}/{storage.database}?authSource=admin"

        try:
            return self.spark_session.read \
                .format("com.mongodb.spark.sql.DefaultSource") \
                .option("spark.mongodb.input.uri", uri) \
                .option("collection", f"{storage.collection}") \
                .load().drop("_id")
        except Exception as err:
            print(err)
            self.__raise(f"Failed to read from mongodb ({uri} - {storage.collection})")

    # write to internal mongodb storage database
    def write_mongodb(self, dataframe: DataFrame, target: MongodbStorage):
        user = target.user
        password = target.password
        auth = ""

        if user and password and (not user.isspace()) and (not password.isspace()):
            auth = f"{user}:{password}@"

        uri = f"mongodb://{auth}{target.host}:{target.port}/{target.database}?authSource=admin"

        try:
            # option for user and password instead of url
            dataframe.write \
                .format("com.mongodb.spark.sql.DefaultSource") \
                .option("spark.mongodb.output.uri", uri) \
                .option("collection", target.collection) \
                .mode("overwrite") \
                .save()
        except Exception as err:
            print(err)
            self.__raise(f"Failed to write collection {target.collection} to internal MongoDB")

    # ==============================================================================================
    # PostgreSQL
    # ==============================================================================================

    # read from any postgresql
    def read_postrgesql(self, storage: PostgresqlStorage) -> DataFrame:
        uri = f"jdbc:postgresql://{storage.host}:{storage.port}/{storage.database}"
        try:
            return self.spark_session.read.jdbc(
                uri,
                table=f'"{storage.table}"',
                properties={
                    "user": storage.user,
                    "password": storage.password,
                    "driver": "org.postgresql.Driver"
                }
            )
        except Exception as err:
            print(err)
            self.__raise(f"Failed to read from postgres ({uri} - {storage.table})")

    # write to internal postgresql storage database
    def write_postgresql(self, dataframe: DataFrame, target: PostgresqlStorage) -> str:
        uri = f"jdbc:postgresql://{target.host}:{target.port}/{target.database}"

        try:
            dataframe.write.jdbc(
                uri,
                table=f'"{target.table}"',
                mode="overwrite",
                properties={
                    "user": self.settings.postgresql_storage.user,
                    "password": self.settings.postgresql_storage.password,
                    "driver": "org.postgresql.Driver"
                }
            )
            return uri
        except Exception as err:
            print(err)
            self.__raise(f"Failed to write table {target.table} to internal PostgreSQL")

    # ==============================================================================================
    # CSV
    # ==============================================================================================

    # read csv file from hdfs
    def read_csv(self, storage: CsvStorage) -> DataFrame:
        hdfs = self.settings.hdfs_storage
        uri = f"hdfs://{hdfs.namenode}:{hdfs.port}/{storage.file}"

        try:
            return self.spark_session.read.csv(
                uri, header=storage.has_header, sep=storage.delimiter, inferSchema=True
            )
        except Exception as err:
            print(err)
            self.__raise(f"Failed to read csv file from hdfs ({uri})")

    # write as csv file to internal hdfs
    def write_csv(self, dataframe: DataFrame, target: CsvStorage) -> str:
        hdfs = self.settings.hdfs_storage
        uri = f"hdfs://{hdfs.namenode}:{hdfs.port}/{target.file}"

        try:
            dataframe.write.csv(
                uri,
                header=target.has_header,
                sep=target.delimiter,
                mode="overwrite"
            )
            return uri
        except Exception as err:
            print(err)
            self.__raise(f"Failed to write csv file {target.file} to internal Hdfs:")

    # ==============================================================================================
    # XML
    # ==============================================================================================

    # read xml file from hdfs
    def read_xml(self, storage: XmlStorage) -> DataFrame:
        hdfs = self.settings.hdfs_storage
        uri = f"hdfs://{hdfs.namenode}:{hdfs.port}/{storage.file}"

        try:
            return self.spark_session.read \
                .format("com.databricks.spark.xml") \
                .option("rowTag", storage.row_tag) \
                .option("rootTag", storage.root_tag) \
                .load(uri)
        except Exception as err:
            print(err)
            self.__raise(f"Failed to read xml file from hdfs ({uri})")

    # write as xml file to internal hdfs
    def write_xml(self, dataframe: DataFrame, target: XmlStorage) -> str:
        hdfs = self.settings.hdfs_storage
        uri = f"hdfs://{hdfs.namenode}:{hdfs.port}/{target.file}"

        try:
            dataframe.write \
                .format("com.databricks.spark.xml") \
                .mode("overwrite") \
                .save(uri)
            return uri
        except Exception as err:
            print(err)
            self.__raise(f"Failed to write xml file {target.file} to internal hdfs")

    # ==============================================================================================
    # JSON
    # ==============================================================================================

    # read json file from  hdfs
    def read_json(self, storage: JsonStorage) -> DataFrame:
        hdfs = self.settings.hdfs_storage
        uri = f"hdfs://{hdfs.namenode}:{hdfs.port}/{storage.file}"

        try:
            return self.spark_session.read.json(uri, multiLine=True)
        except Exception as err:
            print(err)
            self.__raise(f"Failed to read json file from hdfs ({uri})")

    # write as json file to internal hdfs
    def write_json(self, dataframe: DataFrame, target: JsonStorage) -> str:
        hdfs = self.settings.hdfs_storage
        uri = f"hdfs://{hdfs.namenode}:{hdfs.port}/{target.file}"

        try:
            dataframe.write.json(uri, mode="overwrite")
            return uri
        except Exception as err:
            print(err)
            self.__raise("Failed to write json file {file} to internal hdfs")

    # ==============================================================================================
    # Metadata
    # ==============================================================================================

    # read data from internal storage by metadata information
    def read_datamart(self, datamart: Datamart) -> DataFrame:
        target = datamart.metadata.target

        try:
            if isinstance(target, MongodbStorage):
                return self.read_mongodb(target)

            elif isinstance(target, PostgresqlStorage):
                return self.read_postrgesql(target)

            elif isinstance(target, CsvStorage):
                return self.read_csv(target)

            elif isinstance(target, JsonStorage):
                return self.read_json(target)

            elif isinstance(target, XmlStorage):
                return self.read_xml(target)

        except Exception as err:
            print(err)
            self.__raise(f"Failed to read by metadata")

    def write_datamart(self, datamart: Datamart, dataframe: DataFrame):
        target = datamart.metadata.target

        try:
            if isinstance(target, MongodbStorage):
                return self.write_mongodb(dataframe, target)

            elif isinstance(target, PostgresqlStorage):
                return self.write_postgresql(dataframe, target)

            elif isinstance(target, CsvStorage):
                return self.write_csv(dataframe, target)

            elif isinstance(target, JsonStorage):
                return self.write_json(dataframe, target)

            elif isinstance(target, XmlStorage):
                return self.write_xml(dataframe, target)

        except Exception as err:
            print(err)
            self.__raise(f"Failed to read by metadata")
