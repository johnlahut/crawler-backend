# -*- coding: utf-8 -*-
from processor.models import Job
import json

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ScraperPipeline(object):

    def __init__(self, id):
        print('init')
        self.items = []
        self.id = id
        self.job = Job.objects.get(id=self.id)


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
        self.items.append(item['url'])
        return item