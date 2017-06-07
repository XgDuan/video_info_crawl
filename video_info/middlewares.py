# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

import random
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware #代理UA，固定导入
from video_info.settings import USER_AGENTS_POOLS
import  re
# class VideoInfoSpiderMiddleware(object):
#     # Not all methods need to be defined. If a method is not defined,
#     # scrapy acts as if the spider middleware does not modify the
#     # passed objects.
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         # This method is used by Scrapy to create your spiders.
#         s = cls()
#         crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
#         return s
#
#     def process_spider_input(self, response, spider):
#         # Called for each response that goes through the spider
#         # middleware and into the spider.
#
#         # Should return None or raise an exception.
#         return None
#
#     def process_spider_output(self, response, result, spider):
#         # Called with the results returned from the Spider, after
#         # it has processed the response.
#
#         # Must return an iterable of Request, dict or Item objects.
#         for i in result:
#             yield i
#
#     def process_spider_exception(self, response, exception, spider):
#         # Called when a spider or process_spider_input() method
#         # (from other spider middleware) raises an exception.
#
#         # Should return either None or an iterable of Response, dict
#         # or Item objects.
#         pass
#
#     def process_start_requests(self, start_requests, spider):
#         # Called with the start requests of the spider, and works
#         # similarly to the process_spider_output() method, except
#         # that it doesn’t have a response associated.
#
#         # Must return only requests (not items).
#         for r in start_requests:
#             yield r
#
#     def spider_opened(self, spider):
#         spider.logger.info('Spider opened: %s' % spider.name)



# class IPPOOLSMiddleware(HttpProxyMiddleware):
#
#     ip_pools = IP_POOLS
#
#     def __init__(self,ip=''):
#         super(IPPOOLSMiddleware,self).__init__()
#         self.ip = ip
#
#     def process_request(self, request, spider):
#         ip=random.choice(self.ip_pools) #随机选择一个ip
#         print(ip)
#         try:
#             request.meta["proxy"]="http://"+ip
#         except Exception:
#             pass


class UAPOOLSMiddleware(UserAgentMiddleware):

    user_agent_pools = USER_AGENTS_POOLS

    def __init__(self,user_agent=''):
        super(UAPOOLSMiddleware,self).__init__()
        self.user_agent = user_agent

    def process_request(self, request, spider):
        if re.match(r'http://m.iqiyi.com',request.url) is None:
            ua = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'
        else:
            ua = 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1'
        try:
            request.headers.setdefault('User-Agent',ua)
        except Exception:
            pass
