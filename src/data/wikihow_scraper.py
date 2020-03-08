import datetime
import os
import scrapy


class WikiHowSpider(scrapy.Spider):
    name = 'wikihow_search'
    start_urls = [
        'https://www.wikihow.com/Main-Page',
    ]

    def parse(self, response):
        filename = [os.getcwd(),
                    'data/raw',
                    'wikihow-%s.html' %
                    datetime.datetime.now().strftime("%Y-%m-%d")]
        print(filename)
        with open(os.path.join(*filename), 'wb') as f:
            f.write(response.body)
