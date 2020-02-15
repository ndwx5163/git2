from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from book.items import DangDangItem


# mysql> create table t_dangdang(id int(11) primary key auto_increment,title varchar(255) unique,image varchar(255),press varchar(255),info varchar(1000),detail varchar(2000),current_price varchar(20),author varchar(255),num_review varchar(20));
# Query OK, 0 rows affected (0.88 sec)
class DangdangSpider(CrawlSpider):
    """采集当当网图书信息。"""
    name = 'dangdang'
    allowed_domains = ['dangdang.com']
    start_urls = ['http://search.dangdang.com/?key=linux&act=input']

    rules = (
        Rule(LinkExtractor(allow=r'/\?key=linux&act=input&page_index=\d+'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        list_li = response.css('#component_59>li')

        for i in list_li:
            item = DangDangItem()
            item["title"] = i.css('a::attr(title)').get()
            item["image"] = i.css('a>img::attr(src)').get()
            item["info"] = i.css('p[class="name"]>a::attr(title)').get()
            item["detail"] = i.css('p[class="detail"]::text').get()
            item["detail"] = 'no detail' if item["detail"] is None else item["detail"]
            item["current_price"] = i.css('p[class="price"]>span[class="search_now_price"]::text').re_first(
                r'\D+(.+)')
            item["press"] = i.css('p[class="search_book_author"]>span:last-of-type>a::attr(title)').get()
            item["author"] = i.css(
                'p[class="search_book_author"]>span:first-of-type>a:first-of-type::attr(title)').get()
            item["num_review"] = i.css('p[class="search_star_line"]>a[class="search_comment_num"]::text').re_first(
                r'(\d+)\D*')
            yield item
