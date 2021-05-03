from configs.config import Config

# build url for access to storage database in internal mongodb with optional authentication
def mongodbStorageURL(config: Config) -> str:
  host = config.MONGO_HOST
  port = config.MONGO_PORT
  storage = config.STORAGE_NAME
  user = config.MONGO_USER
  password = config.MONGO_PASSWORD
  auth = ""
  if user and password and (not user.isspace()) and (not password.isspace()):
    auth = f"{user}:{password}@"
  return f"mongodb://{auth}{host}:{port}/{storage}?authSource=admin"


# build url for access to strage database in internal postgresql
def postgresStorageURL(config: Config):
  host = config.POSTGRES_HOST
  port = config.POSTGRES_PORT
  storage = config.STORAGE_NAME
  return f"jdbc:postgresql://{host}:{port}/{storage}"


# build url for access to storage in internal hdfs
def hdfsStorageURL(config: Config):
  namenode = config.HDFS_NAMENODE
  port = config.HDFS_PORT
  storage = config.STORAGE_NAME
  return f"hdfs://{namenode}:{port}/{storage}"


def hdfsIngestionURL(config: Config):
  namenode = config.HDFS_NAMENODE
  port = config.HDFS_PORT
  ingestionDir = config.HDFS_INGESTION_DIR
  return f"hdfs://{namenode}:{port}/{ingestionDir}"