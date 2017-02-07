# -*- coding: utf-8 -*-

from classics_spider.items import ClassicsSpiderItem
from scrapy.utils.markup import replace_tags
from scrapy.selector import Selector
from classics_spider.spiders.base import ForumThreadSpider

class ClassicsSpider(ForumThreadSpider):
    name = "classics"
    allowed_domains = ["oldclassiccar.co.uk"]
    start_urls = ['http://www.oldclassiccar.co.uk/forum/phpbb/phpBB2/viewtopic.php?t=12591']

    def __init__(self, *args, **kwargs):
        super(ClassicsSpider, self).__init__(*args, **kwargs)
        self.output_file = kwargs.get("output_file", ClassicsSpider.name)

    def parse(self, response):
        somexpath = "(//span[@class='gensmall'])[1]//a/@href"
        dom = Selector(response)
        links = dom.xpath(somexpath)
        print(links)
        yield ClassicsSpiderItem(
            post_id="test",
            post_author="test",
            post_datetime="test",
            post_content="test"
        )
