# -*- coding: utf-8 -*-

from classics_spider.spiders.base import ForumThreadSpider
from classics_spider.items import ClassicsSpiderItem
from classics_spider.utils import Sanitizer

from scrapy.selector import Selector
from scrapy.http import Request

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
            post_id = post.xpath(XPATHS.POST_ID).extract()
            post_author = Sanitizer.trim(post.xpath(XPATHS.POST_AUTHOR).extract()[0])
            post_datetime = Sanitizer.extract_date(Sanitizer.trim(post.xpath(XPATHS.POST_DATETIME).extract()[0]))
            post_content = Sanitizer.extract_content(Sanitizer.trim(post.xpath(XPATHS.POST_CONTENT).extract()[0]))
            yield ClassicsSpiderItem(
                post_id=post_id,
                post_author=post_author,
                post_datetime=post_datetime,
                post_content=post_content
            )
        if next:
            next_page_url = ClassicsSpider.URL % next.extract()[0]
            print(next_page_url)
            yield Request(
                url=next_page_url,
                callback=self.parse
            )
