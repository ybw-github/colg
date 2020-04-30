# -*- coding: utf-8 -*-
import scrapy
from colg.items import ColgItem

headers={
'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'zh-CN,zh;q=0.9',
'upgrade-insecure-requests': '1',
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
}


class ColgSpider(scrapy.Spider):
    name = 'Colg'
    allowed_domains = ['bbs.colg.cn']
    start_urls = ['https://bbs.colg.cn/forum-171-{}.html'.format(page) for page in range(1,601)]

    def parse(self, response):
        cardIds=response.xpath('//th[@class="new"]/a[1]/@href').extract()
        for cardId in cardIds:
            cardUrl = "https://bbs.colg.cn/"+cardId
            yield scrapy.Request(url=cardUrl, headers=headers, callback=self.parseCard)

    def parseCard(self, response):
        item = ColgItem()
        text = response.xpath('//td[@class="t_f"]/text()').extract()
        text = [i for i in text if i.strip()]
        text = ";".join(text).replace("\n","").replace("\t","").replace("\r","").replace("，","。").replace(",","。")
        beian = response.xpath('//*[@id="flk"]/p[1]/img/@src').re(r'url=/thread-(.*?).html')[0]
        item['cardId'], item['pageId'], item['listId'] = beian.split('-')
        item['text']=text
        yield item
        nxt = response.xpath('//a[@class="nxt"]/@href').extract_first()
        if nxt:
            nxt = "https://bbs.colg.cn/"+nxt
            yield scrapy.Request(url=nxt, headers=headers, callback=self.parseCard)
