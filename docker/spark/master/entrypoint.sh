#!/bin/bash
echo "start spark"
$SPARK_HOME/bin/spark-class org.apache.spark.deploy.master.Master
echo "spark started"