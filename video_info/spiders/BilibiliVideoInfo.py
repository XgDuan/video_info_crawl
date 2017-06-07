# -*- coding: utf-8 -*-
import scrapy
import json
import copy

class BilibilivideoinfoSpider(scrapy.Spider):
    name = 'bilibiliVideoInfo'
    allowed_domains = ['bilibili.com']

    def __init__(self, data_loc):
        super(BilibilivideoinfoSpider,self).__init__()
        self.data_loc = data_loc
        self.url_format1 = 'http://api.bilibili.com/archive_stat/stat?aid=%s&type=jsonp'
        self.url_format2 = 'http://www.bilibili.com/video/av%s/'
        self.url_format3 = 'http://interface.bilibili.com/player?id=cid:18208583&aid=%s'

    def start_requests(self):
        with open(self.data_loc,'r') as data:
            for aid in data.read().splitlines():
                yield scrapy.Request(self.url_format1%(aid), meta={'aid': aid}, callback=self.parse1)

    def parse1(self, response):
        json_response = json.loads(response.body_as_unicode())
        datas= {'aid': response.meta['aid'],
                'playNum': json_response['data']['view'],
                'comment':json_response['data']['reply'],
                'danmu':json_response['data']['danmaku'],
                'like':json_response['data']['favorite'],
        }
        yield scrapy.Request(self.url_format2%(response.meta['aid']),
                              meta={'aid':response.meta['aid'],'datas':datas},
                              callback=self.parse2)

    def parse2(self, response):
        datas =response.meta['datas']
        datas['title'] = response.css('title::text').extract_first()
        datas['issueTime'] =  response.css('time::attr(datetime)').extract_first()
        yield scrapy.Request(self.url_format3%(response.meta['aid']),
                             meta={'aid':response.meta['aid'],'datas':datas},
                             callback=self.parse3)

    def parse3(self, response):
        datas = response.meta['datas']
        datas['duration'] = response.css('duration::text').extract_first()

        yield datas