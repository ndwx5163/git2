import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from image.items import LandscapeItem

class LandscapeSpider(CrawlSpider):
    """大图网高清风景图片下载"""
    name = 'landscape'
    allowed_domains = ['zol.com.cn']
    start_urls = ['http://desk.zol.com.cn/fengjing/']

    rules = (
        Rule(LinkExtractor(allow=r'/bizhi/\d+_\d+_\d\.html'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = LandscapeItem()
        item["image_urls"] = response.css('#bigImg::attr(src)').getall()
        item["name"] = response.css('#titleName::text').get() + response.css('h3 span.current-num::text').get()
        yield item
