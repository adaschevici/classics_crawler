This is a scraper for http://www.oldclassiccar.co.uk/forum/phpbb/phpBB2/viewtopic.php?t=12591

It has been written using the scrapy library : https://scrapy.org/

That provides a quite maintainable and extensible way of running and adding spiders

Requirements can be installed

```
pip install -r requirements.txt
```

Unittests are written using the standard unittest library + requests


The idea is to deploy the spider onto a scrapyd server, however scrapyd and scrapyd-client

is not yet compatible with python 3.6 and needs to be ported to 3.6

To run the unittests :

```
python tests/test_scraper.py
```

To run the crawler:

```
scrapy crawl classic_cars [-a output_file=<file_name>]
```

file_name does not need the csv extension as it already gets it. 

If the filename is missing the created file will be classic_cars.csv
