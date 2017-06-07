# -*- coding: utf-8 -*-
import scrapy
import re
import json

class IqiyivideoinfoSpider(scrapy.Spider):
    name = 'iqiyiVideoInfo'
    allowed_domains = ['iqiyi.com']

    def __init__(self, data_loc):
        super(IqiyivideoinfoSpider, self).__init__()
        self.data_loc = data_loc
        self.url_format0 = 'http://m.iqiyi.com/%s.html'
        self.url_format1 = 'http://www.iqiyi.com/%s.html'
        self.url_format2 = 'http://mixer.video.iqiyi.com/jp/mixin/videos/%s'
        self.url_format3 = 'http://paopao.iqiyi.com/apis/e/starwall/basic_wall.action?authcookie=&device_id=pc_web&agenttype=118&wallId=%s&atoken=8ffffbc44F3tKBShRo5tC9Bm1J5k01EeIqm1jnhIKXLdVMRB2m11Ctom4'
        self.url_format4 = 'http://cmts.iqiyi.com/comment/tvid197/0_%s_hot_2?albumid=5145095310'

    def start_requests(self):
        with open(self.data_loc, 'r') as data:
            for id in data.read().splitlines():
                if re.match(r'/v_[^.]+',id) is not None:
                    # start with v
                    yield scrapy.Request(self.url_format0 % (id), meta={'id': id}, callback=self.parse1)
                else:
                    # start with w
                    yield scrapy.Request(self.url_format1 %(id), meta={'id':id}, callback=self.parse4)

    def parse1(self, response):
        if response.status == '404':
            self.logger.warning('parse1:video not found:404%s'%(response.url))
            return
        raw_data =  response.body_as_unicode()
        try:
            datas = {'id'  :  response.meta['id'],
                     'tvId':  re.search(r'(?<=playInfo.tvid \= ")[^"]+',raw_data).group(0),
                     'vid':  re.search(r'(?<=playInfo.vid \= ")[^"]+',raw_data).group(0),
                     'duration': re.search(r'(?<=playInfo.duration \= ")[^"]+',raw_data).group(0),
                     'title':response.css('title::text').extract_first()
                     # 'issurTime': re.search(r'(?<=playInfo.issueTime \= ")[^"]+',raw_data).group(0),
            }
        except:
            self.logger.warning('parse1:Exception:%s,%s' % (response.url, response.status))
            print(raw_data)
            return
        yield scrapy.Request(self.url_format2 % (datas['tvId']),
                             meta={'id': datas['tvId'],
                                   'datas': datas},
                             callback=self.parse2)


    def parse2(self, response):
        raw_data = re.findall(r'(?<=\=)[\w\W]+',response.body_as_unicode())
        if len(raw_data) ==0:
            self.logger.warning('parse2:Exception:%s,%s'%(response.url,response.status))
            print(response.body_as_unicode())
            return

        json_response = json.loads(raw_data[0])

        datas = response.meta['datas']
        datas['playNum'] = json_response['playCount']
        # datas['duration'] = json_response['duration']
        datas['like'] = json_response['upCount']
        datas['issueTime'] = json_response['issueTime']

        yield scrapy.Request(self.url_format3 % (datas['tvId']),
                             meta={'id':datas['tvId'],
                                   'datas':datas},
                             callback=self.parse3)

    def parse3(self, response):
        json_response = json.loads(response.body_as_unicode())
        if 'msg' in json_response and json_response['code'] == 'P00100':
            datas = response.meta['datas']
            yield scrapy.Request(self.url_format4 % (datas['tvId']),
                                 meta={'id': datas['tvId'],
                                       'datas': datas},
                                 callback=self.parse6)
            return

        datas = response.meta['datas']

        datas['comment'] = json_response['data']['feedCount']

        yield datas

    def parse4(self, response):
        if response.status == '404':
            self.logger.warning('parse4:video not found:404%s'%(response.url))
            return

        raw_data =  response.css('script::text')[8].extract()

        try:
            datas = {'id':response.meta['id'],
                     'vid':   re.search(r'(?<=param\[\'vid\'\] = ")[^"]+',raw_data).group(0),
                     'tvId':  re.search(r'(?<=param\[\'tvid\'\] = ")[^"]+',raw_data).group(0),
                     'title':response.css('title::text').extract_first()
            }

        except:
            self.logger.warning('parse4: Exception:%s,%s' % (response.url, response.status))
            print(raw_data)
            return

        yield scrapy.Request(self.url_format2 % (datas['tvId']),
                             meta={'id': datas['tvId'],
                                   'datas': datas},
                             callback=self.parse5)

    def parse5(self, response):
        raw_data = re.findall(r'(?<=\=)[\w\W]+',response.body_as_unicode())
        if len(raw_data) ==0:
            self.logger.warning('parse5:Exception:%s,%s'%(response.url,response.status))
            print(response.body_as_unicode())
            return

        json_response = json.loads(raw_data[0])

        datas = response.meta['datas']
        datas['playNum'] = json_response['playCount']
        datas['duration'] = json_response['duration']
        datas['like'] = json_response['upCount']
        datas['issueTime'] = json_response['issueTime']

        yield scrapy.Request(self.url_format4 % (datas['tvId']),
                             meta={'id':datas['tvId'],
                                   'datas':datas},
                             callback=self.parse6)

    def parse6(self,response):
        json_response = json.loads(response.body_as_unicode())

        datas = response.meta['datas']
        try:
            datas['comment'] = json_response['data']['$comment$get_video_comments']['data']['count']
        except:
            self.logger.warning('parse6:Exception:%s,%s' % (response.url, response.status))
            return

        yield datas

