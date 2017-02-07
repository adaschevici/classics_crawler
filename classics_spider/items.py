# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ClassicsSpiderItem(scrapy.Item):
    post_id = scrapy.Field()
    post_author = scrapy.Field()
    post_datetime = scrapy.Field()
    post_content = scrapy.Field()
