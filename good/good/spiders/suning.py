import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from good.items import SuningItem


class SuningSpider(scrapy.Spider):
    """采集苏宁易购商品信息。"""
    name = 'suning'
    allowed_domains = ['suning.com']
    max_page = 1

    def start_requests(self):
        start_urls = ['https://search.suning.com/%E6%89%8B%E6%9C%BA/&iy=0&isNoResult=0&cp={}'.format(i) for i in
                      range(SuningSpider.max_page)]
        for i in start_urls:
            yield SeleniumRequest(url=i, wait_time=10, wait_until=EC.element_to_be_clickable((By.ID, 'nextPage')),
                                  script='window.scrollTo(0, document.body.scrollHeight);')

    def parse(self, response):
        list_li = response.css('#product-list>ul[class="general clearfix"]>li')
        for i in list_li:
            item = SuningItem()
            item["title"] = i.css('div[class="title-selling-point"]>a::text').get()
            item["price"] = i.css('span.def-price::text').get()
            item["image"] = i.css('img::attr(src)').get()
            item["num_review"] = i.css('div[class="info-evaluate"]>a>i::text').get()
            item["parameter"] = i.css('div[class="info-config"]::attr(title)').get()
            item["store"] = i.css('div[class="store-stock"]>a::text').get()
            yield item


