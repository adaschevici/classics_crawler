import re
import requests
import sys

from scrapy.http import HtmlResponse, Request
sys.path.append("../classics_spider")

import unittest
from classics_spider.spiders import classics

def fake_response():
    headers = {
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:51.0) Gecko/20100101 Firefox/51.0",
    }
    url = 'http://www.oldclassiccar.co.uk/forum/phpbb/phpBB2/viewtopic.php?t=12591'
    response_body = requests.get(url, headers=headers).text
    request = Request(url=url)
    response = HtmlResponse(
        url=url,
        request=request,
        body=response_body,
        encoding="utf-8"
    )
    return response

class ClassicsSpiderTest(unittest.TestCase):

    def setUp(self):
        self.spider = classics.ClassicsSpider()

    def _test_post_id(self, post_id):
        self.assertIsNotNone(re.match(r'[0-9]{5,9}', post_id))

    def _test_post_author(self, post_author):
        self.assertIsNotNone(re.match(r'[A-Za-z0-9_]+', post_author))

    def _test_post_datetime(self, post_datetime):
        self.assertIsNotNone(re.match(r'[A-Za-z0-9_]+', post_datetime))

    def _test_item_results(self, results, expected_length):
        count = 0
        for item in results:
            try:
                self.assertIsNotNone(item['post_id'])
                self._test_post_id(item['post_id'])
                self.assertIsNotNone(item['post_author'])
                self._test_post_author(item['post_author'])
                self.assertIsNotNone(item['post_content'])
                self.assertIsNotNone(item['post_datetime'])
                self._test_post_datetime(item['post_datetime'])
                count += 1
            except TypeError:
                print("This means the next page is being opened")
                break
        self.assertEqual(count, expected_length)

    def test_parse(self):
        results = self.spider.parse(fake_response())
        self._test_item_results(results, 8)

if  __name__ == "__main__":
    unittest.main()
