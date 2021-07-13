#!/bin/bash
docker build --no-cache -t app:latest .
docker tag app:latest semanticdatalake21/app:latest
docker push semanticdatalake21/app:latest