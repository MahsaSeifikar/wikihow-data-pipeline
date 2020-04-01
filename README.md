# Wikihow Data Pipeline
This project aims to create a trend detection application for WIKIHOW website.
The most important parts of this pipeline are as follows:

    1- Wikihow Crawler
    2- ETL 
    3- The Extraction of interesting knowledge using NLP Algorithms.


## WikiHow Crawler
 In this project, just trend articles will be crawled from the main page of this website. 
 To extract raw data day to day run the following command. 
 
 `scrapy runspider src/data/wikihow_scraper.py
`
## ETL
In order to prepare a structured dataset for data scientists, we run `wikihow_trend_etls.py` which convert all html files in a specific day to CSV file. Each processed CSV file contains the following columns:
1. title
2. last update date
3. date of publishing
4. date of crawling
5. number of views
6. number of votes
7. mean votes
8. main description
9. steps (json)
