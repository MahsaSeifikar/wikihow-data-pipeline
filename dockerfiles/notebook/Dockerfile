FROM ubuntu:latest

RUN \
    apt-get update && \
    apt-get install -y python3 python3-dev python3-pip python3-virtualenv && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get install -y build-essential
RUN pip3 install jupyterlab

RUN pip3 install pyspark
ENV PYSPARK_PYTHON=/usr/bin/python3


COPY requirements.txt /requirements.txt
RUN pip3 install --no-cache-dir -r /requirements.txt

RUN mkdir -p /wikihow_data_pipeline/notebooks

WORKDIR /wikihow_data_pipeline
COPY ./notebooks ./notebooks

COPY dockerfiles/notebook/notebook_run.sh /notebook_run.sh
RUN chmod +x /notebook_run.sh
