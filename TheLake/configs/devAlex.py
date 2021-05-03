import logging
from .dev import DevelopmentConfig
from os import path

class DevelopmentConfigAlex(DevelopmentConfig):
    dockerHost = '192.168.178.55'

    STORAGE_NAME = "datalake_storage"

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
    #JWT_COOKIE_SAMESITE = "None"

    # spark
    SPARK_MASTER = f"spark://{dockerHost}:7077"

    # mongo
    MONGO_HOST = dockerHost
    MONGO_PORT = 27017
    MONGO_USER = "mapro2020"
    MONGO_PASSWORD = "mapro2020"
    MONGO_STORAGE_DB = STORAGE_NAME
    MONGO_ADMINISTRATION_DB = "datalake_administration"
    MONGODB_SETTINGS = {
        "host": f"mongodb://{MONGO_HOST}:{MONGO_PORT}/{MONGO_ADMINISTRATION_DB}",
        "username": MONGO_USER,
        "password": MONGO_PASSWORD,
        "authentication_source": "admin"
    }

    # postgres
    POSTGRES_HOST = dockerHost
    POSTGRES_PORT = 5432
    POSTGRES_USER = "mapro2020"
    POSTGRES_PASSWORD = "mapro2020"
    POSTGRES_STORAGE_DB = STORAGE_NAME

    # file
    HDFS_NAMENODE = "namenode"
    HDFS_PORT=9000
    HDFS_INGESTION_DIR="ingestion_tmp"

    LOG_LEVEL = logging.DEBUG