import datetime
import json
import os
import click
import pandas as pd
from bs4 import BeautifulSoup


def extract(data_path):
    """ Extract a dataframe from html files in data_path

    Args:
        data_path: A path to a folder contains raw html files.

    Returns:
        A dataframe with the following columns:
            1. title
            2. last update date
            3. number of views
            4. number of votes
            5. mean votes
            6. main description
            7. steps (json)
    """
    print('extract')
    df = pd.DataFrame(columns=['title',
                               'date_published',
                               'date_modified',
                               'n_views',
                               'n_votes',
                               'mean_votes',
                               'description',
                               'steps'])
    index = 0
    for file in os.listdir(data_path):
        with open(os.path.join(data_path, file), 'r') as f:
            page_content = f.read()
            soup = BeautifulSoup(page_content, 'html.parser')

            df.loc[index, 'title'] = soup.title.text
            print(soup.title.text)
            for tag in soup.find_all('div', {'class': 'sp_text'}):
                if 'Views:' in str(tag):
                    df.loc[index, 'n_views'] = tag.find('span', {'class': 'sp_text_data'}).text
                    break

            for tag in soup.find_all('script', {'type': "application/ld+json"}):
                tag = tag.text
                if '"step":' in tag:
                    json_obj = json.loads(tag)
                    df.loc[index, 'steps'] = json_obj['step']
                    df.loc[index, 'date_published'] = json_obj['datePublished']
                    df.loc[index, 'date_modified'] = json_obj['dateModified']
                    df.loc[index, 'description'] = json_obj['description']
                    if 'aggregateRating' in json_obj.keys():
                        df.loc[index, 'n_votes'] = json_obj['aggregateRating']['ratingCount']
                        df.loc[index, 'mean_votes'] = json_obj['aggregateRating']['ratingValue']

        index += 1

    return df


def transform(df):
    print('transform')
    return df


def load(df):
    print('load')


@click.command()
@click.option("--project_name", default='trend')
@click.option("--start_date", default='2020-03-23')
@click.option("--end_date", default='2020-03026')
def main(project_name, start_date, end_date):
    data_path = os.path.join(*['data',
                               'raw',
                               project_name])
    with open('config/conf_%s' % project_name, 'r') as f:
        file_names = f.read().split()
    # if file_names is empty run etl from the first available date!
    if not file_names:
        start_date = datetime.datetime.strptime(os.listdir(data_path)[0],
                                                '%Y-%m-%d')
    else:
        start_date = datetime.datetime.strptime(file_names[-1],
                                                '%Y-%m-%d') \
                     + datetime.timedelta(days=1)

    while os.path.exists(os.path.join(data_path,
                                      start_date.strftime('%Y-%m-%d'))):
        print(start_date)

        df = extract(os.path.join(data_path,
                                  start_date.strftime('%Y-%m-%d')))
        print(df['n_votes'])
        # df = transform(df)
        # load(df)
        break
        with open('config/conf_%s' % project_name, 'a') as f:
            f.write(start_date.strftime('%Y-%m-%d'))
            f.write('\n')
        start_date += datetime.timedelta(days=1)


if __name__ == '__main__':
    main()
