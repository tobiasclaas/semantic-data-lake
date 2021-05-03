#!/bin/bash
docker build --no-cache -t spark-worker:latest .
docker tag spark-worker:latest semanticdatalake21/spark-worker:latest
docker push semanticdatalake21/spark-worker