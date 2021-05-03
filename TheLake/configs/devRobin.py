from .dev import DevelopmentConfig
from os import path
import logging

class DevelopmentConfigRobin(DevelopmentConfig):

  dockerHost = "127.0.1.1"

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
  SPARK_MASTER = "local"

  STORAGE_NAME = "datalake_storage"

  # mongo
  MONGO_HOST = dockerHost
  MONGO_PORT = 27017
  MONGO_USER = "mapro2020"
  MONGO_PASSWORD = "mapro2020"
  MONGO_URL = f"mongodb://{MONGO_HOST}:{MONGO_PORT}"
  MONGO_STORAGE_DB = STORAGE_NAME
  MONGO_ADMINISTRATION_DB = "datalake_administration"
  MONGODB_SETTINGS = {
        "host": f"{MONGO_URL}/{MONGO_ADMINISTRATION_DB}",
        "username": MONGO_USER,
        "password": MONGO_PASSWORD,
        "authentication_source": "admin"
  }

  # postgres
  POSTGRES_HOST = dockerHost
  POSTGRES_PORT = 5432
  POSTGRES_URL = f"jdbc:postgresql://{POSTGRES_HOST}:{POSTGRES_PORT}"
  POSTGRES_USER = "mapro2020"
  POSTGRES_PASSWORD = "mapro2020"
  POSTGRES_STORAGE_DB = STORAGE_NAME

  # file
  API_INGESTION_TMP_DIR = "/home/kuller/data-lake/docker-setup/dev/tmp/ingestion"
  SPARK_INGESTION_TMP_DIR = "/tmp/ingestion"
  HDFS_NAMENODE = "namenode"
  HDFS_URI = f"hdfs://{HDFS_NAMENODE}:9000/{STORAGE_NAME}"

  LOG_LEVEL = logging.DEBUG