# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class TesterSpider(CrawlSpider):
    name = 'tester'

    def __init__(self, *args, **kwargs):

        self.url = kwargs.get('url')
        self.domain = kwargs.get('domain')
        self.start_urls = [self.url]
        self.allowed_domains = [self.domain]
        print(f'Starting spider with url: {self.url} and domain: {self.domain}')


        TesterSpider.rules = [
            Rule(LinkExtractor(unique=True), callback='parse_item'),
        ]

        super(TesterSpider, self).__init__(*args, **kwargs)

    # extract data here, pass processing onto pipeline
    def parse_item(self, response):
        item = {}
        item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        item['name'] = response.xpath('//div[@id="name"]').get()
        item['description'] = response.xpath('//div[@id="description"]').get()
        item['url'] = response.url
        return item