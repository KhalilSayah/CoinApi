# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random
# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class ScraperSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)




class ScraperDownloaderMiddleware:
    # Define a list of proxies
    PROXY_LIST = [
    'http://51.158.123.35:8811',
    'http://51.158.68.133:8811',
    'http://51.158.68.103:8811',
    'http://51.158.68.100:8811',
    'http://103.163.182.88:10000',
    'http://143.198.182.218:80',
    'http://185.220.101.40:8080',
    'http://45.152.188.16:3128',
    'http://209.127.191.180:8123',
    'http://51.222.140.172:8080',
]

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Rotate the proxy for each request
        proxy = random.choice(self.PROXY_LIST)
        request.meta['proxy'] = proxy  # Set the proxy for the request
        spider.logger.info(f'Using proxy: {proxy}')  # Log the proxy being used
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.
        return response

    def process_exception(self, request, exception, spider):
        # Handle exceptions
        spider.logger.error(f'Error occurred: {exception}')
        return None

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)
