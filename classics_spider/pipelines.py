# -*- coding: utf-8 -*-
import os
import classics_spider.settings

from scrapy import signals
from scrapy.exceptions import DropItem
from scrapy.exporters import CsvItemExporter
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ClassicsSpiderPipeline(object):

    def __init__(self):
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        item_file = open('%s.csv' % spider.output_file, 'w+b')
        self.files[spider] = item_file
        self.exporter = CsvItemExporter(item_file, delimiter="|")
        self.exporter.fields_to_export = ["post_id", "post_author", "post_datetime", "post_content"]
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        item_file = self.files.pop(spider)
        item_file.close()


    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
