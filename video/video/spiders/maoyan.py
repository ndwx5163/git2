import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from video.items import MaoYanItem


class MaoyanSpider(CrawlSpider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/board/4']

    rules = (
        Rule(LinkExtractor(allow=r'\?offset=\d{2}'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        list_dd = response.xpath('//div[@class="main"]/dl[@class="board-wrapper"]/dd')
        for i in list_dd:
            item = MaoYanItem()
            item["title"] = i.xpath('.//p[@class="name"]/a/@title').get()
            item["star"] = i.xpath('.//p[@class="star"]/text()').get()
            item["release_time"] = i.xpath('.//p[@class="releasetime"]/text()').re_first(r'\D+([\d\-])+')
            item["rank"] = i.xpath('./i[@class]/text()').get()
            yield item
