#!/bin/bash
exec /spark/bin/spark-class org.apache.spark.deploy.worker.Worker spark://$SPARK_MASTER:7077