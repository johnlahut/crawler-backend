# -*- coding: utf-8 -*-
from processor.models import Job
from urllib.parse import urljoin
import json

from .spiders import utils

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ScraperPipeline(object):

    def __init__(self, id):
        print('init')
        self.items = {}
        self.id = id
        self.job = Job.objects.get(id=self.id)
        self.keywords = utils.get_kws('crawler/spiders/run/partner_kw.txt')
        self.stop_words = utils.get_kws('crawler/spiders/run/stop_kw.txt')

        print(self.stop_words)


    # here we init the pipeline with class args from the settings from the django view
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            id=crawler.settings.get('id')
        )

    # set status to in_progress, send message to front-end
    def open_spider(self, spider):
        print(f'opening spider with id {self.id}')
        self.job.status = self.job.IN_PROGRESS
        self.job.save()

    # set status to complete, send message to front-end
    def close_spider(self, spider):
        print('closing spider!')
        self.job.url = json.dumps(self.items)

        if (self.items):
            self.job.status = self.job.COMPLETE
        else:
            self.job.status = self.job.WARNING
        self.job.save()

    # here we do the "heavy-lifting" processing
    def process_item(self, item, spider):

        response_url = item['url']                      # base URL

        for link in item['links']:

            link_url = link.xpath('@href').get()        # piece of link we followed i.e. /partners/
            full_url = urljoin(response_url, link_url)  # base URL and link we followed

            partner = utils.get_hostname(full_url)

            # check to see if we follwed a partner link, and the partner is not in stop words
            if (utils.partner_match(response_url, self.keywords) and
                    not utils.stop_word_match(partner, self.stop_words)):

                # new partner
                if partner not in self.items:
                    self.items[partner] = [response_url]

                # already have partner, just got to it in a different way
                elif partner in self.items and response_url not in self.items[partner]:
                    self.items[partner].append(response_url)


        return item