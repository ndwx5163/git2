"""爬取LOL全英雄名字到mysql"""
import time
from lxml import etree
from selenium import webdriver
import pymysql
import re


# create database db_scrapy charset="utf8mb4";
# use db_scrapy;
# create table t_role(id int primary key auto_increment,name varchar(255));
# create table t_user(id int primary key auto_increment,name varchar(255) unique,role_id int not null);
# alter table t_user add foreign key(role_id) references t_role(id);

class LOL:
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    path_exe = "/home/ndwx/PycharmProjects/chromedriver"
    tuple_id = ((1, "fighter"), (2, "mage"), (3, "tank"), (6, "support"), (4, "assassin"), (5, "marksman"))

    def __init__(self):
        self.client = webdriver.Chrome(executable_path=LOL.path_exe)
        # self.client = webdriver.Chrome(chrome_options=LOL.options,executable_path=LOL.path_exe)
        self.start_url = 'https://lol.qq.com/data/info-heros.shtml'
        self.conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='root', database='db_scrapy',
                                    charset='utf8mb4')
        self.cursor = self.conn.cursor()

    def render_html(self, type):
        # 发送get请求
        self.client.get(self.start_url)
        time.sleep(1)
        str_js = 'document.documentElement.scrollTop=100000'
        self.client.execute_script(str_js)
        time.sleep(5)
        # 获取并且点击该按钮
        obj_id = self.client.find_element_by_xpath('//label[@data-id="{0}"]'.format(type))
        obj_id.click()
        time.sleep(5)

        return self.client.page_source

    def parse(self, str_html, role_id):
        str_html = etree.HTML(str_html)
        list_li = str_html.xpath('//*[@id="jSearchHeroDiv"]/li')
        for li in list_li:
            name = li.xpath('./a/@onclick')[0]
            tuple_content = re.findall(r"'heros(\d+)','(.*?)'", name)[0]  # 第一个元素是下标，第二个元素是名字
            tuple_new = (tuple_content[0], tuple_content[1], role_id)  # 第一个元素是下标，第二个元素是名字，第三个元素是外键
            yield tuple_new

    def save_role(self):
        for i in LOL.tuple_id:
            sql = 'insert into t_role (id,name) values ("{0}","{1}")'.format(i[0], i[1])
            self.cursor.execute(sql)
            self.conn.commit()

    def save(self, gen0):
        for i in gen0:
            sql = 'insert into t_user (name,role_id) values ("{0}","{1}")'.format(i[1], i[2])
            try:
                self.cursor.execute(sql)
            except pymysql.err.IntegrityError:
                print("{}，该英雄已经存在了...".format(i[1]))
                self.conn.rollback()
            else:
                self.conn.commit()
                print("{}，插入成功...".format(i[1]))

    def run(self):
        self.save_role()
        for _, i in LOL.tuple_id:
            r = self.render_html(i)
            gen0 = self.parse(r, _)  # 获得该类型的生成器
            self.save(gen0)  # 传递生成器，添加字段

    def __del__(self):
        self.cursor.close()
        self.conn.close()
        self.client.close()


o = LOL()
o.run()
