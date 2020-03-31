import datetime
import os
import scrapy


class WikiHowSpider(scrapy.Spider):
    name = 'wikihow_trend_detection'
    main_url = 'https://www.wikihow.com'
    start_urls = [
        main_url + '/Main-Page',
    ]

    def parse(self, response):
        request_list = response.xpath('//div[@id="hp_popular"]/'
                                      'div[@id="hp_popular_container"]/'
                                      'div[@class="hp_thumb "]/'
                                      'a/@href').getall()
        for request in request_list:
            yield response.follow(self.main_url + request,
                                  callback=self.parse_subpage)

    def parse_subpage(self, response):
        title = response.xpath('//title/text()').extract_first()
        path = os.path.join(*[os.getcwd(),
                              'data',
                              'raw',
                              'trend',
                              datetime.datetime.now().strftime("%Y-%m-%d")])

        if not os.path.exists(path):
            os.makedirs(path)
        with open(os.path.join(path, title), 'wb') as f:
            f.write(response.body)
