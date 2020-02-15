import scrapy
from book.items import QiDianItem


class QidianSpider(scrapy.Spider):
    """起点中文网小说数据采集。"""
    name = 'qidian'
    allowed_domains = ['qidian.com']
    start_urls = ['https://book.qidian.com/info/1017696480#Catalog']

    def parse(self, response):
        list_li = response.css('ul[class="cf"]>li[data-rid]')
        for i in list_li:
            item = QiDianItem()
            item["href"] = i.css('a::attr(href)').get()
            item["name_chapter"] = i.css('a::text').re_first(r'\d+\.(.+)')
            item["num_chapter"] = i.css('a::text').re_first(r'(\d+)\..+')
            item["first_time"] = i.css('a::attr(title)').re_first(r'\D+([\d\-\s:]+)\D+\d+').strip()
            item["num_character"] = i.css('a::attr(title)').re_first(r'\D+[\d\-\s:]+\D+(\d+)')
            if item['href']:
                yield scrapy.Request('https:' + item["href"], callback=self.second_parse, meta={"item": item})

    def second_parse(self, response):
        item = response.meta["item"]
        item["content"] = '\n'.join(
            [i.strip() for i in response.css('div[class="read-content j_readContent"]>p::text').getall()])
        yield item
