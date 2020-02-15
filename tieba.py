"""百度贴吧——梦幻西游吧爬取，将数据保存到mongodb。"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from lxml import etree
import json
import pymongo


class TB:
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    start_url = 'https://tieba.baidu.com/f?kw=%C3%CE%BB%C3%CE%F7%D3%CE&fr=ala0&tpl=5'
    mongo_uri = 'mongodb://127.0.0.1:27017/admin'
    db_name = 'db_scrapy'
    collection_name = 'c_tieba_mhxy'

    def __init__(self):
        self.client=webdriver.Chrome(chrome_options=TB.options,executable_path="/home/ndwx/PycharmProjects/chromedriver")
        # self.client = webdriver.Chrome(executable_path="/home/ndwx/PycharmProjects/chromedriver")
        self.mongo = pymongo.MongoClient(TB.mongo_uri)
        self.c = self.mongo[TB.db_name][TB.collection_name]

    def render_html(self):
        self.client.get(TB.start_url)
        time.sleep(2)
        str_js = 'document.documentElement.scrollTop=100000'
        self.client.execute_script(str_js)
        time.sleep(5)

    def parse(self, html):
        obj_html = etree.HTML(html)
        list_li = obj_html.xpath('//*[@id="thread_list"]/li')
        for i in list_li:
            item = {}
            item["title"] = i.xpath('.//a[@class="j_th_tit "]/text()')
            item["title"] = item["title"][0] if len(item["title"]) else ''
            item["author"] = i.xpath('.//span[@class="tb_icon_author "]/@title')
            item["author"] = item["author"][0] if len(item["author"]) else ''
            item["content"] = i.xpath(
                './div[@class="t_con cleafix"]/div[@class="col2_right j_threadlist_li_right "]/div[@class="threadlist_detail clearfix"]/div[@class="threadlist_text pull_left"]/div[1]/text()')
            item["content"] = item["content"][0].strip() if len(item["content"]) else ''
            item["reply"] = i.xpath('.//span[@class="threadlist_rep_num center_text"]/text()')
            item["reply"] = item["reply"][0] if len(item["reply"]) else ''
            item["last_reply"] = i.xpath('.//span[@class="tb_icon_author_rely j_replyer"]/@title')
            item["last_reply"] = item["last_reply"][0] if len(item["last_reply"]) else ''
            item["update_time"] = i.xpath('.//span[@class="threadlist_reply_date pull_right j_reply_data"]/text()')
            item["update_time"] = item["update_time"][0].strip() if len(item["update_time"]) else ''
            print(json.dumps(item, ensure_ascii=False, indent=4))
            yield item

    def render_next(self):
        button = self.client.find_element_by_xpath('//*[@id="frs_list_pager"]/a[@class="next pagination-item "]')
        button.send_keys(Keys.ENTER)

    def main(self):
        self.render_html()
        self.c.insert_many(self.parse(self.client.page_source))
        for i in range(9):
            print(10 * '{}'.format(i + 2))
            self.render_next()
            self.render_html()
            self.c.insert_many(self.parse(self.client.page_source))

    def __del__(self):
        self.client.close()


o = TB()
o.main()
