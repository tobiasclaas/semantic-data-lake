from .dev import DevelopmentConfig
import logging

class DevelopmentConfigMarcel(DevelopmentConfig):
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

  # mongo
  MONGO_HOST = "127.0.0.1"
  MONGO_PORT = "27017"
  MONGO_URL = f"mongodb://{MONGO_HOST}:{MONGO_PORT}"
  MONGO_PASSWORD = ""
  MONGO_USER = ""
  MONGO_STORAGE_DB = "dataLakeStorage"

  # postgres
  POSTGRES_HOST = "127.0.0.1"
  POSTGRES_PORT = "5432"
  POSTGRES_URL = f"jdbc:postgresql://{POSTGRES_HOST}:{POSTGRES_PORT}"
  POSTGRES_USER = "postgres"
  POSTGRES_PASSWORD = "2311"
  POSTGRES_STORAGE_DB = "dataLakeStorage"

  
  MONGO_ADMINISTRATION_DB = "dataLakeAdministration"
  MONGODB_SETTINGS = {"host": f"{MONGO_URL}/{MONGO_ADMINISTRATION_DB}"}
  LOG_LEVEL = logging.DEBUG

  '''logging.basicConfig(
    filename=os.getenv("SERVICE_LOG", "server.log"),
    level=logging.DEBUG,
    format="%(levelname)s: %(asctime)s \
      pid:%(process)s module:%(module)s %(message)s",
    datefmt="%d/%m/%y %H:%M:%S",
  )'''