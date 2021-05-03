#!/bin/bash
docker build --no-cache -t spark-base:latest .
docker tag spark-base:latest semanticdatalake21/spark-base:latest
docker push semanticdatalake21/spark-base:latest