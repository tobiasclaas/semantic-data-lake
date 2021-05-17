FROM python:3.9

ENV SPARK_HOME /spark

RUN wget https://downloads.apache.org/spark/spark-3.1.1/spark-3.1.1-bin-hadoop3.2.tgz && \
  tar -xzf spark-3.1.1-bin-hadoop3.2.tgz && \
  mv spark-3.1.1-bin-hadoop3.2 spark && \
  rm spark-3.1.1-bin-hadoop3.2.tgz

RUN wget -O /spark/jars/postgresql-42.2.18.jar https://jdbc.postgresql.org/download/postgresql-42.2.18.jar

RUN apt-get update && apt-get upgrade -y
RUN apt-get install software-properties-common -y
RUN apt-add-repository 'deb http://security.debian.org/debian-security stretch/updates main'
RUN apt-get update
RUN apt-get install openjdk-8-jdk -y