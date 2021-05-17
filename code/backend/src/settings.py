import os
import yaml


class PostgresqlStorage:
    def __init__(self, host, port, database, user, password):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password


class MongodbStorage:
    def __init__(self, host, port, database, user=None, password=None):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password


class HdfsStorage:
    def __init__(self, namenode, port, ingestion_directory, storage_directory):
        self.namenode = namenode
        self.port = port
        self.ingestion_directory = ingestion_directory
        self.storage_directory = storage_directory


class Settings(object):

    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(Settings, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    spark_master = ""

    postgresql_storage: PostgresqlStorage = None
    mongodb_storage: MongodbStorage = None
    hdfs_storage: HdfsStorage = None


def load(server):
    #config_path = os.environ.get('/home/mapro2020/refactor/team-2-data-lake/datalake_config.yml')
    config_file = open('../../../datalake_config.yml')
    config_data = yaml.load(config_file, yaml.FullLoader)

    jwt = config_data.get("jwt")
    server_mongodb = config_data.get("serverMongodb")
    static_path = "../../frontend/public"
    host = server_mongodb.get("host")
    port = server_mongodb.get("port")
    mongo_db = server_mongodb.get("database")

    server.config.update(
        SECRET_KEY=jwt.get("secretKey"),
        JWT_SECRET_KEY=jwt.get("secretKey"),
        JWT_TOKEN_LOCATION=jwt.get("tokenLocation"),
        JWT_ACCESS_CSRF_HEADER_NAME=jwt.get("accessCsrfHeaderName"),
        JWT_COOKIE_CSRF_PROTECT=jwt.get("cookieCsrfProtect"),
        JWT_ACCESS_TOKEN_EXPIRES=jwt.get("accessTokenExpires"),
        JWT_REFRESH_TOKEN_EXPIRES=jwt.get("refreshTokenExpires"),
        MONGODB_SETTINGS={
            "host": f"mongodb://{host}:{port}/{mongo_db}",
            "username": server_mongodb.get("user"),
            "password": server_mongodb.get("password"),
            "authentication_source": "admin"
        }
    )

    settings = Settings()

    settings.spark_master = config_data.get("sparkMaster")

    pg_data = config_data.get("storages").get("postgresql")
    settings.postgresql_storage = PostgresqlStorage(
        pg_data.get("host"),
        pg_data.get("port"),
        pg_data.get("database"),
        pg_data.get("user"),
        pg_data.get("password"),
    )

    m_data = config_data.get("storages").get("mongodb")
    settings.mongodb_storage = MongodbStorage(
        m_data.get("host"),
        m_data.get("port"),
        m_data.get("database"),
        m_data.get("user"),
        m_data.get("password"),
    )

    hdfs_data = config_data.get("storages").get("hdfs")
    settings.hdfs_storage = HdfsStorage(
        hdfs_data.get("namenode"),
        hdfs_data.get("port"),
        hdfs_data.get("ingestionDirectory"),
        hdfs_data.get("storageDirectory")
    )
