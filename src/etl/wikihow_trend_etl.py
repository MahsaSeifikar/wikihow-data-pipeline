import json
import os
from pathlib import Path

import click
from bs4 import BeautifulSoup
import pandas as pd

from utils.setup_logging import logger


def extract(abs_path, dir_name):
    """ Extract a dataframe from html files in data_path

    Args:
        abs_path: A path to a folder contains raw html files.
        dir_name: folder name contains raw htlm files

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
    data_path = os.path.join(abs_path, dir_name)
    for file in os.listdir(data_path):
        with open(os.path.join(data_path, file), 'r') as f:
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
    df['date_crawled'] = dir_name
    logger.info('All files in this path %s/%s are extracted' % (abs_path, dir_name))
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


def load(df, data_path, filename):
    """ Save dataframe to a csv file in processed folder

    Args:
        df: a clean dataframe.
        data_path: path to raw folder.
        filename: A string that is a date for saving data.
    Return:
        Nothing!
    """

    data_path = data_path.replace('raw', 'processed')
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    df.to_csv(os.path.join(data_path, filename + '.csv'))
    logger.info('The dataframe is loaded in this path %s are extracted' % data_path)


@click.command()
@click.option("--project_name", default='trend')
def main(project_name):
    abs_path = os.path.dirname(os.path.dirname(os.getcwd()))
    data_path = os.path.join(*[abs_path,
                               'data',
                               'raw',
                               project_name])
    with open(abs_path + '/config/conf_%s' % project_name, 'r') as f:
        processed_dir_list = f.read().split()
    # Sort path based on modification date and remove the dir that already processed
    current_paths = sorted(Path(data_path).iterdir(), key=os.path.getmtime)
    current_paths = [str(path).split('/')[-1] for path in current_paths]
    current_dir_list = set(current_paths) - set(processed_dir_list)

    for filename in current_dir_list:
        df = extract(data_path, filename)
        df = transform(df)
        load(df, data_path, filename)

        # Save the current day as a processed day.
        with open(abs_path + '/config/conf_%s' % project_name, 'a') as f:
            f.write(filename)
            f.write('\n')


if __name__ == '__main__':
    main()
