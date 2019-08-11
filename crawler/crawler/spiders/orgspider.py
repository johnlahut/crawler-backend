import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from . import utils

import os

class OrgSpider(CrawlSpider):
    name = 'orgspider'

    def __init__(self, *args, **kwargs):

        self.url = kwargs.get('url')
        self.domain = kwargs.get('domain')
        self.start_urls =  ['https://www.unitedwaygcr.org']# [self.url]
        self.allowed_domains = ['www.unitedwaygcr.org']# [self.domain]


        OrgSpider.rules = [
            Rule(LinkExtractor(unique=True), callback='parse_item')
        ]

        super(OrgSpider, self).__init__(*args, **kwargs)

    # extract data from request, pass to pipeline to do processing
    def parse_item(self, response):
        item = {}
        url = response.url
        base = utils.get_hostname(url)

        item['links'] = response.xpath('//a')
        item['url'] = url
        item['base'] = base
        return item
