"""爬取包图网短视频，保存到本地。"""
import requests
import time
from lxml import etree


class Video:
    start_url = 'https://ibaotu.com/shipin/7-5023-0-0-0-1.html'
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"}

    def parse(self, html):
        obj_html = etree.HTML(html)
        list_li = obj_html.xpath('//div[@class="media-list"]/ul["clearfix sucai_list"]/li')
        for i in list_li:
            item = {}
            item["name"] = i.xpath('./@pr-data-title')[0]
            item["src"] = 'https:' + i.xpath('.//div[@class="video-play"]/video/@src')[0]
            print(item)
            yield item

    def save(self, title, content):
        with open('./video/{}.mp4'.format(title), 'wb') as file:
            file.write(content)

    def main(self):
        r = requests.get(Video.start_url, headers=Video.headers)
        for i in self.parse(r.content.decode("U8")):
            print("{}.............".format(i["name"]))
            time.sleep(3)
            r = requests.get(i["src"], headers=Video.headers)
            self.save(i["name"], r.content)


o = Video()
o.main()
