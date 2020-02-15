import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from good.items import GoodItem


class JdSpider(scrapy.Spider):
    """采集京东商城商品信息。"""
    name = 'jd'
    allowed_domains = ['jd.com']

    def start_requests(self):
        start_urls = [
            'https://search.jd.com/Search?keyword=%E7%AC%94%E8%AE%B0%E6%9C%AC%E7%94%B5%E8%84%91&enc=utf-8&suggest=1.def.0.V06--12s0,20s0,38s0,97s0&wq=%E7%AC%94%E8%AE%B0%E6%9C%AC&pvid=e786017dad2c43cbb04712cafc03a8e8']
        for i in start_urls:
            yield SeleniumRequest(url=i, wait_time=5, wait_until=EC.element_to_be_clickable((By.CLASS_NAME, 'pn-next')),
                                  script='document.documentElement.scrollTop=100000;')

    def parse(self, response):
        list_li = response.css('#J_goodsList>ul[class="gl-warp clearfix"]>li')
        for i in list_li:
            item = GoodItem()
            item["name"] = '\n'.join(
                i.css('div[class="gl-i-wrap"]>div[class="p-name p-name-type-2"]>a>em::text').getall())
            item["price"] = i.css(
                'div[class="gl-i-wrap"]>div[class="p-price"]>strong>i::text').get()
            item["store"] = i.css('div[class="gl-i-wrap"]>div[class="p-shop"]>span>a::attr(title)').get()
            item["num_review"] = i.css('div[class="gl-i-wrap"]>div[class="p-commit"]>strong>a::text').get()
            item["image"] = i.css('div[class="gl-i-wrap"]>div[class="p-img"]>a>img::attr(data-lazy-img)').get()
            yield item
