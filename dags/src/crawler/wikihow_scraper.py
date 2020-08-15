import logging
import datetime
import os
import scrapy
from scrapy.crawler import CrawlerProcess

from src.utils.setup_logging import get_costum_logger

logger = get_costum_logger(logging.getLogger(__name__))

class WikiHowSpider(scrapy.Spider):
    name = 'wikihow_trend_detection'
    main_url = 'https://www.wikihow.com'
    start_urls = [
        main_url+'/Main-Page',
    ]

    def parse(self, response):
        request_list = response.xpath('//div[@id="hp_popular"]/'
                                      'div[@id="hp_popular_container"]/'
                                      'div[@class="hp_thumb  "]/'
                                      'a/@href').getall()
        for request in request_list:
            yield response.follow(self.main_url + request,
                                  callback=self.parse_subpage)

    def parse_subpage(self, response):
        title = response.xpath('//title/text()').extract_first()
        path = os.path.join(*['/wikihow_data_pipeline',
                              'data',
                              'raw',
                              'wikihow_trend',
                              datetime.datetime.now().strftime("%Y-%m-%d")])
        if not os.path.exists(path):
            os.makedirs(path)
        with open(os.path.join(path, title), 'wb') as f:
            f.write(response.body)
            logger.info(f'{title} page is already crawled!')



def run_crawler(**kwargs):
    process = CrawlerProcess()
    process.crawl(WikiHowSpider)
    process.start() 