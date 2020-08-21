FROM ubuntu:latest

RUN \
    apt-get update && \
    apt-get install -y python3 python3-dev python3-pip python3-virtualenv && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install pyspark
ENV PYSPARK_PYTHON=/usr/bin/python3


COPY requirements.txt /requirements.txt
RUN pip3 install --no-cache-dir -r /requirements.txt

RUN apt-get update && \
    apt-get -y install sudo

# install apache-airflow
RUN pip3 install apache-airflow


RUN mkdir -p /wikihow_data_pipeline/dags
RUN mkdir -p /wikihow_data_pipeline/data/log
CMD touch /wikihow_data_pipeline/data/log/logging.log
RUN chmod 777 /wikihow_data_pipeline/data

WORKDIR /wikihow_data_pipeline
COPY ./dags ./dags

COPY dockerfiles/airflow/airflow.cfg /wikihow_data_pipeline/airflow.cfg
COPY dockerfiles/airflow/airflow_run.sh /airflow_run.sh
RUN chmod 777 /airflow_run.sh

