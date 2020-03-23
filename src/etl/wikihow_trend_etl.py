import click


def extract(project_name, start_date, end_date):
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
@click.option("--end_date", default='2020-03024')
def main(project_name, start_date, end_date):
    df = extract(project_name, start_date, end_date)
    df = transform(df)
    load(df)
