#!/bin/bash
docker build --no-cache -t backend:latest .
docker tag backend:latest semanticdatalake21/backend:latest
docker push semanticdatalake21/backend