# -*- coding: utf-8 -*-

from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.loader import ItemLoader

from classics_spider.spiders.base import ForumThreadSpider
from classics_spider.items import ClassicsSpiderItem
from classics_spider.utils import Sanitizer

class XPATHS:

    NEXT_PAGE = "(//span[@class='gensmall'])[1]//a[contains(.,'Next')]/@href"
    POSTS_LIST = "//table[@class='forumline']//tr[./td[@class='row1' and @valign='top']]" # "//table[@class='forumline']//tbody"
    POST_ID = ".//span[@class='name']/a/@name"
    POST_AUTHOR = ".//span[@class='name']/b"
    POST_DATETIME = ".//table//span[@class='postdetails']"
    POST_CONTENT = ".//span[@class='postbody']"

class ClassicsSpider(ForumThreadSpider):
    URL = "http://www.oldclassiccar.co.uk/forum/phpbb/phpBB2/%s"
    name = "classic_cars"
    allowed_domains = ["oldclassiccar.co.uk"]
    start_urls = ['http://www.oldclassiccar.co.uk/forum/phpbb/phpBB2/viewtopic.php?t=12591']

    def __init__(self, *args, **kwargs):
        super(ClassicsSpider, self).__init__(*args, **kwargs)
        self.output_file = kwargs.get("output_file", ClassicsSpider.name)

    def start_requests(self):
        urls = [
            'http://www.oldclassiccar.co.uk/forum/phpbb/phpBB2/viewtopic.php?t=12591'
        ]
        for url in urls:
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        dom = Selector(response)
        next = dom.xpath(XPATHS.NEXT_PAGE)
        posts = dom.xpath(XPATHS.POSTS_LIST)
        for post in posts:
            loader = ItemLoader(item=ClassicsSpiderItem(), selector=post)
            loader.add_xpath('post_id', XPATHS.POST_ID)
            loader.add_xpath('post_author', XPATHS.POST_AUTHOR)
            loader.add_xpath('post_datetime', XPATHS.POST_DATETIME)
            loader.add_xpath('post_content', XPATHS.POST_CONTENT)
            yield loader.load_item()
        if next:
            next_page_url = ClassicsSpider.URL % next.extract()[0]
            print(next_page_url)
            yield Request(
                url=next_page_url,
                callback=self.parse
            )
