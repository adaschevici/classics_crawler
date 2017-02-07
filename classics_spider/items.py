# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import Join, MapCompose, TakeFirst
from w3lib.html import remove_tags

from classics_spider.utils import Sanitizer


class ClassicsSpiderItem(scrapy.Item):
    post_id = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=Join(),
    )
    post_author = scrapy.Field(
        input_processor=MapCompose(remove_tags, Sanitizer.trim),
        output_processor=Join(),
    )
    post_datetime = scrapy.Field(
        input_processor=MapCompose(remove_tags, Sanitizer.extract_date),
        output_processor=Join(),
    )
    post_content = scrapy.Field(
        input_processor=MapCompose(remove_tags, Sanitizer.extract_content),
        output_processor=Join(),
    )
