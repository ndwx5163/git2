import scrapy
from scrapy_splash import SplashRequest
from good.items import GZItem


class GzSpider(scrapy.Spider):
    """采集瓜子二手车汽车信息。"""
    name = 'gz'
    allowed_domains = ['guazi.com']
    script_lua = '''
            function main(splash,args)
                splash.images_enabled=False
                splash:go(args.url)
                splash:wait(1)
                splash.scroll_postion= {y=99999}
                splash:wait(3)
                return splash:html()
            end
        '''

    def start_requests(self):
        start_urls = ['https://www.guazi.com/huainan/buy/o{}/#bread'.format(i) for i in range(1, 4)]
        for i in start_urls:
            yield SplashRequest(url=i, endpoint='execute', args={"lua_source": GzSpider.script_lua})

    def parse(self, response):
        list_li = response.xpath('//ul[@class="carlist clearfix js-top"]/li')
        for i in list_li:
            item = GZItem()
            item["title"] = i.xpath('./a/@title').get()
            item["image"] = i.xpath('./a/img/@src').get()
            item["price"] = i.xpath('./a/div[@class="t-price"]/p/text()').get() + 'w'
            item["info"] = i.xpath('./a/div[@class="t-i"]/text()').getall()
            yield item
