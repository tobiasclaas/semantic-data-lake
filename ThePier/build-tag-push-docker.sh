#!/bin/bash
docker build --no-cache -t pier:latest .
docker tag pier:latest semanticdatalake21/pier:latest
docker push semanticdatalake21/pier