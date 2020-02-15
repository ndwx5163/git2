import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from good.items import JSItem


class JsSpider(CrawlSpider):
    """简书网全站爬取，但是只有title和article两个字段不是通过JS加载的，其他字段是JS加载，如果想要通过crawlspider，必须重写crawlspider内部的某些发送请求的方法。。"""
    name = 'js'
    allowed_domains = ['jianshu.com']
    start_urls = ['https://www.jianshu.com/']

    rules = (
        Rule(LinkExtractor(allow=r'/p/\w+'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = JSItem()
        item["title"] = response.xpath('//h1[@class="_1RuRku"]/text()').get()
        item["article"] = response.xpath('//article[@class="_2rhmJa"]/p/text()').getall()
        yield item

