# Wikihow Data Pipeline
This project aims to create a data pipeline for WIKIHOW website.
The most important parts of this pipeline are as follows:

    1- Crawler
    2- ETL
    3- Data Analysis
    4- REST API

In this project, I employ the following technologies to design my pipeline:

    1- Apache Airflow: to crawl data, do ETL on raw data and extract funny information
    2- Postgresql: to save information.
    3- Flask API: to send a request to server  to ger information


## 1- WikiHow Crawler
 In this project, just trend articles will be crawled from the main page of this website. 
 To extract raw data day to day you just need to turn the ` wikihow_trend_crawler ` dag on!

![AirFlow Dags](../assets/airflow_dags.png?raw=true)
 
## 2- ETL
In order to prepare a structured dataset for data scientists, we turn `wikihow_trend_etls ` dag on which convert all html files in a specific day to CSV file. Each processed CSV file contains the following columns:
1. title
2. last update date
3. date of publishing
4. date of crawling
5. number of views
6. number of votes
7. mean votes
8. main description
9. steps (json)


## 3- Data Analysis
under development

## 4- Rest API
under development


# How to run?
You just need to run the following command to make everything done. note that you should install docker before.

    `docker-compose up --build`
