#!/bin/bash
docker build --no-cache -t pier:refactor .
docker tag pier:refactor semanticdatalake21/pier:refactor
docker push semanticdatalake21/pier:refactor