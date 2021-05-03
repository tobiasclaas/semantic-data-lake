#!/usr/bin/python3

import findspark
findspark.init()
from pyspark.sql import SparkSession
import os


# Create SparkSession
spark = SparkSession.builder \
    .master("spark://master:7077") \
    .appName("File Connector") \
    .config('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector_2.12:3.0.0,org.postgresql:postgresql:42.2.18,com.databricks:spark-xml_2.12:0.10.0') \
    .getOrCreate()


# TODO Infer Schema muss angegeben werden (aus Metadaten lesen)
# TODO variablen delimiter

# Read CSV from Hadoop

hdfs_path = "dataLakeStorage/csvFiles/f91dcb60-0f7f-4a8e-9fe9-5b4394cd6ded"

df = spark.read \
    .format("csv") \
    .option("delimiter", ";") \ 
    .option('header', True) \
    .option("inferSchema", True) \
    .load(hdfs_path)

df.show()
df.printSchema()


# TODO Infer Schema muss angegeben werden (aus Metadaten lesen)
# Read JSON from Hadoop

hdfs_path = "dataLakeStorage/jsonFiles/132bfae4-55bb-430d-a045-77d2c6f66ddc/"

df = spark.read \
    .option("multiline", True) \
    .json(hdfs_path)

df.show()
df.printSchema()


# TODO Infer Schema muss angegeben werden (aus Metadaten lesen)
# TODO Stichpunkt: rowTag und rootTag -> Was? Warum? Wofür? Wie setzen?
# Read XML from Hadoop

hdfs_path = "dataLakeStorage/xmlFiles/8aa28ec7-60e0-4931-a99f-926974084c44/"

df = spark.read \
    .format("com.databricks.spark.xml") \
    .option("rowTag", "Match") \
    .load(hdfs_path)

df.show()
df.printSchema()
