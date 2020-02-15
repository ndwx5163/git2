import scrapy
from book.items import ZongHengItem


class ZonghengSpider(scrapy.Spider):
    """采集纵横网小说数据"""
    name = 'zongheng'
    allowed_domains = ['zongheng.com']
    start_urls = ['http://book.zongheng.com/showchapter/907701.html']

    def parse(self, response):
        list_li = response.xpath('//ul[@class="chapter-list clearfix"]/li')
        for i in list_li:
            item = ZongHengItem()
            item["href"] = i.xpath('./a/@href').get()
            if item["href"]:
                yield scrapy.Request(item["href"], callback=self.second_parse, meta={'item': item})

    def second_parse(self, response):
        item = response.meta.get('item')
        item["content"] = '\n'.join([i.strip() for i in response.xpath('//div[@class="content"]/p/text()').getall()])
        item["num_character"] = response.xpath('//div[@class="bookinfo"]/span[1]/text()').get()
        item["time_update"] = response.xpath('//div[@class="bookinfo"]/span[2]/text()').get()
        item["num_chapter"] = response.xpath('//div[@class="title_txtbox"]/text()').re_first(r'(\S+)\s\S+')
        item["name_chapter"] = response.xpath('//div[@class="title_txtbox"]/text()').re_first(r'\S+\s(\S+)')
        yield item
