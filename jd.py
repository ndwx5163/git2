"""爬取JD商品信息"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from lxml import etree


class JD:
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    start_url = 'https://search.jd.com/Search?keyword=%E7%94%B5%E8%84%91&enc=utf-8&wq=%E7%94%B5%E8%84%91&pvid=1e88f46c19a74009b8440356a5b7d6bb'

    def __init__(self):
        # 创建一个浏览器对象，需要指定该驱动所在的绝对路径
        self.client = webdriver.Chrome(chrome_options=JD.options,
                                       executable_path="/home/ndwx/PycharmProjects/chromedriver")

    def render_html(self, url=None):
        # 发送get请求
        if url is not None:
            self.client.get(url)
        time.sleep(5)
        # 将页面拉到底
        str_js = 'document.documentElement.scrollTop=100000'
        self.client.execute_script(str_js)
        time.sleep(5)
        return self.client.page_source

    def parse(self, str_html):
        # 将页面格式化
        obj_r = etree.HTML(str_html)
        list_li = obj_r.xpath('//*[@id="J_goodsList"]/ul[@class="gl-warp clearfix"]/li')

        for li in list_li:
            item = {}
            item["price"] = li.xpath('./div[@class="gl-i-wrap"]/div[@class="p-price"]/strong/i/text()')[0]
            item["name"] = "".join(li.xpath('./div[@class="gl-i-wrap"]/div[contains(@class,"p-name")]/a/em/text()'))
            item["sales"] = li.xpath('./div[@class="gl-i-wrap"]/div[@class="p-commit"]/strong/a/text()')[0]

            yield item

        self.button_next_page = self.client.find_element_by_xpath(
            '//*[@id="J_bottomPage"]/span[@class="p-skip"]/a[@class="btn btn-default"]')

    def next(self):
        self.button_next_page.send_keys(Keys.ENTER)

    def main(self):
        html = self.render_html(JD.start_url)
        for i in self.parse(html):
            print(i)
        self.next()

        for i in range(3):
            print(10 * '{}'.format(i + 2))
            html = self.render_html()
            for i in self.parse(html):
                print(i)
            self.next()

    def __del__(self):
        self.client.close()


o = JD()
o.main()
