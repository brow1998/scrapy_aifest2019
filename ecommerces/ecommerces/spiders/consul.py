# -*- coding: utf-8 -*-
import scrapy
import json
import re
from urllib import parse
from scrapy.spiders import SitemapSpider
from datetime import datetime

class ConsulSpider(SitemapSpider):
    name = 'consul'
    sitemap_urls = [
        'http://loja.consul.com.br/sitemap.xml',
    ]
    sitemap_rules = [
        (r'/p$', 'parse_product'),
    ]

    def parse_product(self, response):
        if ('ProductLinkNotFound' in response.request.url) or ('/404?' in response.request.url):
            return None

        data = json.loads(re.findall(r'vtex.events.addData\((.*)\);', response.text)[0].replace('&quot;','"'))

        try:
            photo_url = re.findall(r':\"https?://[a-z]{3,50}\.vteximg\.com\.br\/arquivos\/ids/[0-9]{3,7}-[0-9]{3,4}-[0-9]{3,4}/.{3,200}\.[a-z]{3,4}',response.text)[0].replace(':"','')
        except:
            photo_url = response.xpath('//img[@productindex="0"]/@src').extract()[0]

        yield {
            "url": response.url,
            "status_code" : response.status,
            "store": "CONSUL",
            "data": data,
            "photo_url": photo_url,
            "created_at": datetime.now(),
        }
