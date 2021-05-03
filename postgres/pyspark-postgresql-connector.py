#!/usr/bin/python3

import findspark
findspark.init()
from pyspark.sql import SparkSession
import configparser
import uuid

# Create SparkSession
jar_path = "postgres/drivers/postgresql-42.2.18.jar"

spark = SparkSession.builder \
    .master("spark://master:7077") \
    .appName("Postgres Connector") \
    .config("spark.jars", jar_path) \
    .getOrCreate()


# Create the Database properties

db_properties={}
config = configparser.ConfigParser()
config.read("postgres/db_properties.ini")
db_prop = config['postgres']
db_properties['username'] = db_prop['username']
db_properties['password'] = db_prop['password']
db_properties['url'] = db_prop['url']
db_properties['driver'] = db_prop['driver']

print("db_properties:")
print(db_properties)

# Read Table in Dataframe

df = spark.read \
    .format("jdbc") \
    .option("url", db_properties['url']) \
    .option("dbtable", "test_table") \
    .option("user", db_properties['username']) \
    .option("password", db_properties['password']) \
    .option("driver", db_properties['driver']) \
    .load()

print(df.printSchema())


# Write the Dataframe to the DataLake Postgres Table
uid= uuid.uuid4()
properties2 = {"user": "postgres","password": "admin", "driver": "org.postgresql.Driver"} 
df.write.jdbc(url=db_properties['url'], table='"{}"'.format(str(uid)), mode='overwrite', properties=properties2)
