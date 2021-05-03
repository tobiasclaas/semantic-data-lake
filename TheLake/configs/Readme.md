# Configs
A list of all variables to configure the server. Variables with a star are required to be set.

## Flask

## Common
STORAGE_NAME: This name will be used for the storage databases for MongoDB and PostgreSQL and for the Hdfs folder

## MongoDB
Configuration of the internal MongoDB

| Varibale                | Use         |
| ----------------------- | ----------- |
| MONGO_HOST              | Host        |
| MONGO_PORT              | Port        |
| MONGO_USER              | User        |
| MONGO_PASSWORD          | Password for MONGO_USER |
| MONGO_ADMINSITRATION_DB | Database for storing administration data of the server
| MONGODB_SETTINGS        | Settings for the MonogDB framework of flask |
