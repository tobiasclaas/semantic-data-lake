FROM python:3.9
COPY . /app
WORKDIR /app

RUN apt-get update && apt-get upgrade -y && apt-get install default-jre -y

RUN pip install -r requirements.txt

ENV IN_DOCKER=True
WORKDIR /app/src
ENTRYPOINT python server.py