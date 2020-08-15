import json
import os
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
from bs4 import BeautifulSoup

from src.utils.setup_logging import logger


def extract(raw_data_path):
    """ Extract a dataframe from html files in data_path

    Args:
        raw_data_path: A path to a folder contains raw html files.

    Returns:
        A dataframe with the following columns:
            1. title
            2. last update date
            3. date of publishing
            4. date of crawling
            5. number of views
            6. number of votes
            7. mean votes
            8. main description
            9. steps (json)
    """

    df = pd.DataFrame(columns=['date_crawled',
                               'title',
                               'date_published',
                               'date_modified',
                               'n_views',
                               'n_votes',
                               'mean_votes',
                               'description',
                               'steps'])
    index = 0
    for file in os.listdir(raw_data_path):
        with open(os.path.join(raw_data_path, file), 'r') as f:
            page_content = f.read()
            soup = BeautifulSoup(page_content, 'html.parser')

            df.loc[index, 'title'] = soup.title.text
            df.loc[index, 'description'] = soup.find('div', {'class': 'mf-section-0'}).text
            for tag in soup.find_all('div', {'class': 'sp_text'}):
                if 'Views:' in str(tag):
                    df.loc[index, 'n_views'] = tag. \
                        find('span', {'class': 'sp_text_data'}).text
                    break

            for tag in soup.find_all('script',
                                     {'type': "application/ld+json"}):
                tag = tag.text
                if '"step":' in tag:
                    json_obj = json.loads(tag)
                    df.loc[index, 'steps'] = json_obj['step']
                    df.loc[index, 'date_published'] = json_obj['datePublished']
                    df.loc[index, 'date_modified'] = json_obj['dateModified']
                    if 'aggregateRating' in json_obj.keys():
                        df.loc[index, 'n_votes'] = \
                            json_obj['aggregateRating']['ratingCount']
                        df.loc[index, 'mean_votes'] = \
                            json_obj['aggregateRating']['ratingValue']

        index += 1
    df['date_crawled'] = raw_data_path.split('/')[-1]
    logger.info(f'All files in this path {raw_data_path} are extracted ')
    return df


def transform(df):
    """ Clean raw data_frame by the following steps:
        1. Removing space characters
        2. Fill nan value
        3. Specify column types

    Arg:
        df: A raw dataframe

    Return:
        A clean dataframe
    """
    df = df.fillna(0)
    numerical_columns = ['n_views', 'n_votes', 'mean_votes']
    df[numerical_columns] = df[numerical_columns].replace(',', '')
    df['date_published'] = pd.to_datetime(df['date_published'],
                                          format='%Y-%m-%d')
    df['date_modified'] = pd.to_datetime(df['date_modified'],
                                         format='%Y-%m-%d')
    df['description'] = df['description'].replace(r'\n\r', ' ')
    df['steps'] = df['steps'].replace(r'\n\r', ' ')

    return df


def load(df, processed_data_path):
    """ Save dataframe to a csv file in processed folder

    Args:
        df: a clean dataframe.
        processed_data_path: path to processed folder.
    Return:
        Nothing!
    """

    if not os.path.exists(processed_data_path):
        os.makedirs(processed_data_path)
    df.to_csv(os.path.join(processed_data_path, 'wikihow_trends.csv'))
    logger.info(f'The dataframe is loaded in this' 
                f'path {processed_data_path} are extracted')


def run_etl(raw_data_path, processed_data_path, **kwargs):
    
    df = extract(raw_data_path)
    df = transform(df)
    load(df, processed_data_path)

