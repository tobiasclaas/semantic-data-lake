#!/bin/bash
docker build --no-cache -t backend:refactor .
docker tag backend:refactor semanticdatalake21/backend:refactor
docker push semanticdatalake21/backend:refactor