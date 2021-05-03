#!/bin/bash
echo "start spark"
cd /spark/bin
./spark-class org.apache.spark.deploy.master.Master
echo "spark started"