FROM ubuntu:20.04
COPY /code /app
WORKDIR /app

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get upgrade -y && apt-get install -y default-jre software-properties-common npm
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt install -y python3.9 && apt install -y python3-pip

RUN pip install -r backend/requirements.txt

WORKDIR /app/frontend
RUN npm install
RUN npm run build

WORKDIR /app/backend/src/