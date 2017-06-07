# -*- coding: utf-8 -*-
import scrapy
import json

import re

class YoukuvideoinfoSpider(scrapy.Spider):
    name = 'youkuVideoInfo'
    allowed_domains = ['youku.com']

    custom_settings = {
        'DOWNLOAD_DELAY':1
    }
    def __init__(self, data_loc):
        super(YoukuvideoinfoSpider, self).__init__()
        self.data_loc = data_loc
        self.url_format1 = 'http://v.youku.com/v_show/id_%s.html'
        self.url_format2 = 'http://p.comments.youku.com/ycp/comment/pc/commentList?jsoncallback=n_commentList&app=100-DDwODVkv&objectId=%s&objectType=1&listType=0&currentPage=1&pageSize=30&sign=c1e6c741e56afee4be050b448222a28b&time=1496724732'
        self.url_format3 = 'http://v.youku.com/action/getVideoPlayInfo?beta&timestamp=1496741346259&vid=%s&showid=%s&param%%5B%%5D=share&param%%5B%%5D=favo&param%%5B%%5D=download&param%%5B%%5D=phonewatch&param%%5B%%5D=updown&callback=tuijsonp5'

    def start_requests(self):
        with open(self.data_loc, 'r') as data:
            for id in data.read().splitlines():
                yield scrapy.Request(self.url_format1 % (id), meta={'id2': id}, callback=self.parse1)

    def parse1(self, response):
        if 'y404' in response.url:
            self.logger.warning('video not found:404%s'%(response.url))
            return
        raw_data =  response.css('script::text')[6].re(r'(?<=PageConfig =)[^;]+')
        if len(raw_data) ==0:
            self.logger.warning('Exception:%s,%s'%(response.url,response.status))
            print(response.body_as_unicode())
            return
        try:
            datas = {'id':   re.findall(r'(?<=videoId:")[^"]+',raw_data[0])[0],
                     'id2':  re.findall(r'(?<=videoId2:")[^"]+',raw_data[0])[0],
                     'duration': re.findall(r'(?<=seconds:")[^"]+',raw_data[0])[0],
                     'title':response.css('title::text').extract_first()
            }
        except:
            self.logger.warning('Exception:%s,%s' % (response.url, response.status))
            return
        yield scrapy.Request(self.url_format2 % (datas['id']),
                             meta={'id': datas['id'],
                                   'showid':re.findall(r'(?<=showid:")[^"]+',raw_data[0])[0],
                                   'datas': datas},
                             callback=self.parse2)

    def parse2(self, response):
        raw_data = re.findall(r'(?<=\()[^\)]+',response.body_as_unicode())
        if len(raw_data) ==0:
            self.logger.warning('Exception:%s,%s'%(response.url,response.status))
            print(response.body_as_unicode())
            return

        json_response = json.loads(raw_data[0])

        datas = response.meta['datas']
        datas['comment'] = json_response['data']['totalSize']
        yield scrapy.Request(self.url_format3 % (response.meta['id'], response.meta['showid']),
                             meta={'id':datas['id'],
                                   'datas':datas},
                             callback=self.parse3)

    def parse3(self, response):
        datas = response.meta['datas']
        try:
            json_response = json.loads(re.findall(r'(?<=\()[^\)]+', response.body_as_unicode())[0])['data']
        except:
            self.logger.warning('Exception:%s,%s'%(response.url,response.status))
            # print(response.body_as_unicode())

        datas['playNum'] = json_response['stat']['vv']
        datas['like']    = json_response['updown']['up']

        yield datas