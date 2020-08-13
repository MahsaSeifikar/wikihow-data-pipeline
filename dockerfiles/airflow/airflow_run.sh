#!/bin/sh


set -o errexit
set -o nounset

airflow initdb

sleep 5

airflow webserver -p 8000 & sleep 5 & airflow scheduler

