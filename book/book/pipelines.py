import pymysql


class QiDianPipeline:
    def process_item(self, item, spider):
        if spider.name == "qidian":
            print(item)
        return item


class ZongHengPipeline:
    def process_item(self, item, spider):
        if spider.name == "zongheng":
            print(item)
        return item


class DangDangPipeline:
    dict_db = {
        "host": "127.0.0.1",
        "port": 3306,
        "user": "root",
        "password": "root",
        "database": "db_scrapy",
        "charset": "utf8mb4"
    }

    def __init__(self):
        self.conn = pymysql.Connect(**DangDangPipeline.dict_db)
        self.cursor = self.conn.cursor()
        self.sql = 'insert into t_dangdang (title,image,press,info,detail,current_price,author,num_review) values ("{}","{}","{}","{}","{}","{}","{}","{}")'

    def close_spider(self):
        self.cursor.close()
        self.conn.close()

    def process_item(self, item, spider):
        if spider.name == "dangdang":
            print(item)
            try:
                self.cursor.execute(
                    self.sql.format(item["title"], item["image"], item["press"], item["info"], item["detail"],
                                    item["current_price"], item["author"], item["num_review"]))
            except pymysql.IntegrityError:
                print('这本书已经存在了')
                self.conn.rollback()
            except Exception:
                print('error')
                self.conn.rollback()
            else:
                self.conn.commit()
        return item
