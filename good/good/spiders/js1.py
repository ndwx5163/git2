import scrapy
from scrapy_selenium import SeleniumRequest
from good.items import JSItem

class Js1Spider(scrapy.Spider):
    """简书网文章信息采集，采集到JS加载上去的数据，但是这种方式不容易做到全站爬取。"""
    name = 'js1'
    allowed_domains = ['jianshu.com']

    def start_requests(self):
        start_urls = ['https://www.jianshu.com/p/3e90d39e24ff']
        for i in start_urls:
            yield SeleniumRequest(url=i, wait_time=10, script='window.scrollTo(0, document.body.scrollHeight);')

    def parse(self, response):
        item = JSItem()
        item["title"] = response.xpath('//h1[@class="_1RuRku"]/text()').get()
        item["author"] = response.xpath('//span[@class="FxYr8x"]/a[@class="_1OhGeD"]/text()').get()
        item["num_diamond"] = response.xpath('//span[@class="_3tCVn5"]/span/text()').get()
        item["date"] = response.xpath('//time/text()').re_first(r'([\d\.]+)\s[\d:]+')
        item["time"] = response.xpath('//time/text()').re_first(r'[\d\.]+\s([\d:]+)')
        item["num_character"] = response.xpath('//div[@class="s-dsoj"]/span[2]/text()').re_first(r'\D+([\d,]+)')
        item["num_read"] = response.xpath('//div[@class="s-dsoj"]/span[3]/text()').re_first(r'\D+([\d,]+)')
        item["article"] = response.xpath('//article[@class="_2rhmJa"]/p/text()').getall()
        yield item
