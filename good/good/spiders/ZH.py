import scrapy
from good.items import ZHItem


class ZHSpider(scrapy.Spider):
    """登陆知乎网站采集数据。"""
    name = 'zh'
    allowed_domains = ['zhihu.com']
    cookie_raw = '_zap=e32e91f0-9687-4440-9fd0-67f005019da7; _xsrf=q4LdTX0dhFQGuabvGuefbGeMkOCvIayx; d_c0="ABAc7beGzxCPThmfGwq28gYBDcyirycYkyA=|1581584757"; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1581584758; capsion_ticket="2|1:0|10:1581584758|14:capsion_ticket|44:Mjg0NTk1NTkwMzIxNDU1YTlmNTExZDhkMTk5MDI1OWY=|384874a9c5418ee881d11e87dc5f9dc6e4edc4b900eda89ee843cfbcd5770eb6"; z_c0="2|1:0|10:1581584793|4:z_c0|92:Mi4xU2NZNEJRQUFBQUFBRUJ6dHQ0YlBFQ1lBQUFCZ0FsVk5tVjh5WHdEYXJqQmNKd0xLTUljZ3BSa0RXUms3R0pFNVVn|0988023e396c50684632af4957ec2844d14f23742ae0f4fdcf41673feceeeebb"; unlock_ticket="ADDCQpIV7QsmAAAAYAJVTaEYRV58MeByqofkIlZZbDHMOEkZv-0CFg=="; tst=r; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1581584801; KLBRSID=0a401b23e8a71b70de2f4b37f5b4e379|1581584908|1581584753'
    cookie = {i.split('=')[0]: i.split('=')[1] for i in cookie_raw.split('; ')}

    def start_requests(self):
        start_urls = ['https://www.zhihu.com/']
        for i in start_urls:
            yield scrapy.Request(url=i, cookies=ZHSpider.cookie)

    def parse(self, response):
        list_div = response.css(
            'div[class="Topstory-recommend"]>div[class]>div[class="Card TopstoryItem TopstoryItem-isRecommend"]')
        for i in list_div:
            item = ZHItem()
            item["title"] = i.css('h2 a::text').get()
            item["one_review"] = i.css(
                'div[class="RichContent is-collapsed"] span[class="RichText ztext CopyrightRichText-richText"]::text').get()
            item["num_agree"] = i.css(
                'div[class="RichContent is-collapsed"]>div[class="ContentItem-actions"]>span>button[class="Button VoteButton VoteButton--up"]::attr(aria-label)').re_first(
                r'\D+([\d\.K]+)')
            item["num_review"] = i.css(
                'div[class="RichContent is-collapsed"]>div[class="ContentItem-actions"]>button[class="Button ContentItem-action Button--plain Button--withIcon Button--withLabel"]::text').re_first(
                r'(\d+)\D+')
            yield item
