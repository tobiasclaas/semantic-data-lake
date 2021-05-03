#!/usr/bin/python3

import findspark
findspark.init()
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, monotonically_increasing_id, col
import os
import uuid

# Postgres DB properties
POSTGRE_HOST = "postgres"
POSTGRE_PORT = "5432"
POSTGRE_USER = "postgres"
POSTGRE_PASSWORD = "admin"

# Mongo DB properties
MONGO_HOST = "mongodb"
MONGO_PORT = "27017"

# SELECT FILE:
filename = "Bundesliga_2013_Matches.csv"
#filename = "Bundesliga_2013_TeamData.json"
# filename = "Bundesliga_2013_MatchData.xml"

# Split the extension from the path and normalize it to lowercase.
extension = os.path.splitext(filename)[-1].lower()

# Create a unique identifier for table/collection-names in databases
uid = uuid.uuid4()

# Create SparkSession
spark = SparkSession.builder \
    .master("spark://master:7077") \
    .appName("File Connector") \
    .config('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector_2.12:3.0.0,org.postgresql:postgresql:42.2.18,com.databricks:spark-xml_2.12:0.10.0') \
    .getOrCreate()


#--------------------------------------------------------------------------------------
# CSV-FILES:
if extension == ".csv":
    print("processing csv-File...")
    
    # Read CSV in Dataframe
    filePath = "/plain_files/data/" + filename

    df = spark.read \
        .format("csv") \
        .option("delimiter", ";") \
        .option("header", True) \
        .option("inferSchema", True) \
        .load(filePath)

    df.show()
    df.printSchema()

    #-----------------------------------------------
    # Write CSV into DataLake Postgres Table
    print("writing CSV to Postgres...")
    
    mode = "overwrite"
    url = "jdbc:postgresql://{}:{}/test_db".format(POSTGRE_HOST, POSTGRE_PORT)
    properties = {"user": POSTGRE_USER, "password": POSTGRE_PASSWORD, "driver": "org.postgresql.Driver"}

    df.write.jdbc(url=url, table='"{}"'.format(str(uid)), mode=mode, properties=properties)

    print("Write to Postgres succeeded!")

    #-----------------------------------------------
    # TODO Write CSV into HDFS
    # print("writing CSV to HDFS...")
    # hdfsPath = "dataLakeStorage/csvFiles/" + str(uid)

    # df.write.mode('overwrite') \
    #     .option('header', True) \
    #     .csv(hdfsPath)
    
    # print("Write to hdfs succeeded!")

    #dfNew = spark.read.format("csv").option("delimiter", ";").option('header', True).option("inferSchema", True).load(hdfsPath)

    #dfNew.show()
    

#--------------------------------------------------------------------------------------
# JSON-FILES:
elif extension == ".json":
    print("processing json-File...")

    # Read JSON in DataFrame
    filePath = "plain_files/data/" + filename

    df = spark.read \
        .option("multiline", True) \
        .json(filePath)

    df.show()
    df.printSchema()

    #-----------------------------------------------
    # Write JSON into DataLake MongoDB 
    # print("writing JSON to MongoDB...")
    # mongoPath = "mongodb://{}:{}".format(MONGO_HOST, MONGO_PORT)

    # df.write.format("mongo") \
    #     .option("database","dataLakeStorage") \
    #     .option("collection", uid) \
    #     .option("spark.mongodb.output.uri", mongoPath)\
    #     .mode("overwrite") \
    #     .save()

    # print("Write to MongoDB succeeded!")
    
    #-----------------------------------------------
    # Write JSON into HDFS
    
    print("writing JSON to HDFS...")
    hdfsPath = "hdfs://namenode:9000/dataLakeStorage/csvFiles/" + str(uid) + extension

    data = [('First', 1), ('Second', 2), ('Third', 3), ('Fourth', 4), ('Fifth', 5)]
    df = spark.createDataFrame(data)

    df.write \
        .mode("overwrite") \
        .csv(hdfsPath)
    
    print("Write to HDFS succeeded!")
    
    #-----------------------------------------------
    # Write MongoDB data to dataframe
    '''
    print("Reading from MongoDB into dataframe...")
    dbName = "dataLakeStorage"
    # collectionName = uid
    collectionName = "61e09766-3738-4d1a-b838-cc8fb73ac5bf"

    dfMongo = spark.read.format("com.mongodb.spark.sql.DefaultSource")\
        .option("spark.mongodb.input.uri", mongoPath)\
        .option("database", dbName)\
        .option("collection", collectionName)\
        .load()
    dfMongo.show()
    dfMongo.printSchema()

    #-----------------------------------------------
    # "flatten data" - example for this data 
    print("flatten data")
    dfExploded = dfMongo\
        .select(explode("season.TeamData").alias("seasonX"))\
        .select(explode("seasonX.PlayerData").alias("player"), col("seasonX.TeamName").alias("TeamName"))\
        .select(col("player.Player_Name").alias("PlayerName"), "TeamName")\
        .withColumn("PlayerID", monotonically_increasing_id())
    dfExploded.show()

    #-----------------------------------------------
    # Do an easy SQL request on the dataframe
    print("starting SQL Part")
    sqlRequest =   "SELECT * FROM teamData\
                    WHERE TeamName like 'bayern%'\
                    ORDER BY PlayerName"


    dfExploded.createOrReplaceTempView("teamData")

    dfDataMart = spark.sql(sqlRequest)
    dfDataMart.show()
    print("end of SQL Part")

    #-----------------------------------------------
    # Save the new dataframe as a DataMart to MongoDB
    print("writing DataMart DataFrame to MongoDB...")
    uidNew = uuid.uuid4()

    dfDataMart.write.format("mongo") \
        .option("database","dataLakeStorage") \
        .option("collection", uidNew) \
        .option("spark.mongodb.output.uri", mongoPath)\
        .mode("overwrite") \
        .save()

    print("Write DataMart to MongoDB succeeded!")

    #-----------------------------------------------
    # Read DataMart in DataFrame and show it
    
    print("Read DataMart and show it")
    collectionNameNew = uidNew

    dfDataMartRead = spark.read.format("com.mongodb.spark.sql.DefaultSource")\
        .option("spark.mongodb.input.uri", mongoPath)\
        .option("database", dbName)\
        .option("collection", collectionNameNew)\
        .load()

    dfDataMartRead.show()
    dfDataMartRead.printSchema()
    '''
#--------------------------------------------------------------------------------------
# XML-FILES:
elif extension == ".xml":
    print("processing xml-File...")
    
    # Read XML in DataFrame
    # filePath = "plain_files/data/" + filename

    # df = spark.read \
    #     .format("com.databricks.spark.xml") \
    #     .option("rowTag", "Match") \
    #     .load(filePath)
    #     #rowTag und rootTag have to be choosed correctly
    # df.printSchema()

    #-----------------------------------------------
    # Write XML into DataLake MongoDB
    # print("writing XML to MongoDB...")
    mongoPath = "mongodb://{}:{}".format(MONGO_HOST, MONGO_PORT)

    # df.write \
    #     .format("mongo") \
    #     .option("database","dataLakeStorage") \
    #     .option("collection", uid) \
    #     .option("spark.mongodb.output.uri", mongoPath) \
    #     .mode("overwrite") \
    #     .save()

    # print("Write to MongoDB succeeded!")
    #-----------------------------------------------
    # Write XML into HDFS
    # print("writing XML to HDFS...")
    # hdfsPath = "dataLakeStorage/xmlFiles/" + str(uid)

    # df.select("*").write \
    #     .format("com.databricks.spark.xml") \
    #     .option("rowTag", "Match") \
    #     .mode("overwrite") \
    #     .save(hdfsPath)
    
    # print("Write to HDFS succeeded!")

    #-----------------------------------------------
    # Write MongoDB data to dataframe
    print("Reading from MongoDB into dataframe...")
    user = ""
    password = ""
    dbName = "dataLakeStorage"
    # collectionName = uid
    collectionName = "b0d51ca6-dae9-4267-ad1f-8f1f8d7f14e1"

    dfMongo = spark.read.format("com.mongodb.spark.sql.DefaultSource")\
        .option("spark.mongodb.input.uri", mongoPath)\
        .option("database", dbName)\
        .option("collection", collectionName)\
        .load()
    #dfMongo.show()
    dfMongo.printSchema()
        # .option("user", user)\
        # .option("password", password)\
    
    #-----------------------------------------------
    # Do an easy SQL request on the dataframe
    print("starting SQL Part")
    sqlRequest =   "SELECT * FROM matchData"


    dfMongo.createOrReplaceTempView("matchData")

    dfSql = spark.sql(sqlRequest)
    dfSql.show()
    print("end of SQL Part")
#--------------------------------------------------------------------------------------
# Unsupported File-Type
else:
    print("Filetype not supported!")
