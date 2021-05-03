from .prod import ProductionConfig
from os import environ

class ProductionConfigDocker(ProductionConfig):
    ENVIRONMENT = "Dev"
    DEBUG = True
    TESTING = False
    HOST = "0.0.0.0"
    PORT = 5000
    
    SECRET_KEY = "thewildbrownbear"
    JWT_SECRET_KEY = "thewildbrownbear"
    JWT_TOKEN_LOCATION = ["cookies"]
    JWT_ACCESS_CSRF_HEADER_NAME = "X-CSRF-TOKEN-ACCESS"
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_ACCESS_TOKEN_EXPIRES = 90000000000
    JWT_REFRESH_TOKEN_EXPIRES = 90000000000

    # spark
    SPARK_MASTER = "spark://{}:7077".format(environ.get("SPARK_MASTER"))

    STORAGE_NAME = environ.get("STORAGE_NAME", "datalake_storage")

    # mongo
    MONGO_HOST = environ.get("MONGO_HOST")
    MONGO_PORT = environ.get("MONGO_PORT")
    MONGO_USER = environ.get("MONGO_INITDB_ROOT_USERNAME")
    MONGO_PASSWORD = environ.get("MONGO_INITDB_ROOT_PASSWORD")
    MONGO_STORAGE_DB = environ.get("MONGO_STORAGE_DB", STORAGE_NAME)
    MONGO_ADMINISTRATION_DB = environ.get("MONGO_ADMINISTRATION_DB", "datalake_administration")
    MONGODB_SETTINGS = {
        "host": f"mongodb://{MONGO_HOST}:{MONGO_PORT}/{MONGO_ADMINISTRATION_DB}",
        "username": MONGO_USER,
        "password": MONGO_PASSWORD,
        "authentication_source": "admin"
    }


    # postgres
    POSTGRES_HOST = environ.get("POSTGRES_HOST")
    POSTGRES_PORT = environ.get("POSTGRES_PORT")
    POSTGRES_USER = environ.get("POSTGRES_USER")
    POSTGRES_PASSWORD = environ.get("POSTGRES_PASSWORD")
    POSTGRES_STORAGE_DB = environ.get("POSTGRES_STORAGE_DB", STORAGE_NAME)

    # file
    HDFS_NAMENODE = environ.get("HDFS_NAMENODE")
    HDFS_PORT=environ.get("HDFS_PORT")
    HDFS_INGESTION_DIR=environ.get("HDFS_INGESTION_DIR", "ingestion_tmp")

    pass