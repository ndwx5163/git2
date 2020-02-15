import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from video.items import VideoItem


class DoubanSpider(CrawlSpider):
    name = 'douban'
    allowed_domains = ['douban.com']
    start_urls = ['https://movie.douban.com/top250']

    rules = (
        Rule(LinkExtractor(allow=r'\?start=\d+&filter='), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        list_li = response.css('div[class="article"]>ol[class="grid_view"]>li')
        for i in list_li:
            item = VideoItem()
            item["title"] = i.css('div[class="item"]>div[class="info"]>div[class="hd"]>a>span::text').getall()
            item["rank"] = i.css('div[class="item"]>div[class="pic"]>em::text').get()
            item["role"] = i.css('div[class="item"] div[class="bd"]>p::text').get()
            item["score"] = i.css('div[class="item"] span[class="rating_num"]::text').get()
            item["num_review"] = i.css('div[class="item"] div[class="star"]>span:last-of-type::text').re_first(
                r'(\d+)\D+')
            item["theme"] = i.css('div[class="item"] div[class="bd"]>p[class="quote"]>span[class="inq"]::text').get()

            yield item

