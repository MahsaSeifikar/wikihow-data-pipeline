import datetime
import os
import click


def extract(project_name, start_date):
    """ Extract

    """
    print('extract')

    df = ''
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

        # df = extract(project_name, start_date)
        # df = transform(df)
        # load(df)

        with open('config/conf_%s' % project_name, 'a') as f:
            f.write(start_date.strftime('%Y-%m-%d'))
            f.write('\n')
        start_date += datetime.timedelta(days=1)


if __name__ == '__main__':
    main()
