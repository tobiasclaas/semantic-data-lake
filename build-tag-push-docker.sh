#!/bin/bash
rm -rf docker/dev/data docker/full/data
docker build --no-cache -t app:latest .
docker tag app:latest semanticdatalake21/app:latest
docker push semanticdatalake21/app:latest