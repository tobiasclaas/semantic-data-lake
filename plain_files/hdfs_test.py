from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .master("spark://192.168.178.55:7077") \
    .appName("Test") \
    .config('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector_2.12:3.0.0,org.postgresql:postgresql:42.2.18,com.databricks:spark-xml_2.12:0.10.0') \
    .getOrCreate()

dataframe = spark.read \
    .format("com.mongodb.spark.sql.DefaultSource") \
    .option("spark.mongodb.input.uri", "mongodb://mapro2020:mapro2020@192.168.178.55:27017/datalake_storage?authSource=admin") \
    .option("collection", "2b1d4474-f2e7-4319-b8e4-40ecc027397d") \
    .load()

dataframe.createOrReplaceTempView("json")

dataframe = spark.read \
    .format("com.databricks.spark.xml") \
    .option("rowTag", "Match") \
    .load("hdfs://namenode:9000/datalake_storage/xml/e7648d49-721f-48b8-88ea-2467e7c1af83.xml")

dataframe.printSchema()

dataframe.createOrReplaceTempView("xml")

dataframe = spark.sql("SELECT * FROM xml JOIN json")

dataframe.printSchema()

dataframe.write.json()