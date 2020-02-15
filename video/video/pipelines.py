import pymongo


class VideoPipeline:
    collection_name = 'c_douban'

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db


    def open_spider(self, spider):
        if spider.name == "douban":
            self.client = pymongo.MongoClient(self.mongo_uri)
            self.c = self.client[self.mongo_db][VideoPipeline.collection_name]

    def close_spider(self, spider):
        if spider.name == "douban":
            self.client.close()

    def process_item(self, item, spider):
        if spider.name == "douban":
            self.c.insert_one(dict(item))
            print(item)
        return item

class MaoYanPipeline:
    collection_name = 'c_maoyan'

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db


    def open_spider(self, spider):
        if spider.name == "maoyan":
            self.client = pymongo.MongoClient(self.mongo_uri)
            self.c = self.client[self.mongo_db][MaoYanPipeline.collection_name]

    def close_spider(self, spider):
        if spider.name == "maoyan":
            self.client.close()

    def process_item(self, item, spider):
        if spider.name == "maoyan":
            self.c.insert_one(dict(item))
            print(item)
        return item