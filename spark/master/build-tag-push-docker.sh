#!/bin/bash
docker build --no-cache -t spark-master:latest .
docker tag spark-master:latest semanticdatalake21/spark-master:latest
docker push semanticdatalake21/spark-master