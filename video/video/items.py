import scrapy


class VideoItem(scrapy.Item):
    title = scrapy.Field()
    role = scrapy.Field()
    rank = scrapy.Field()
    num_review = scrapy.Field()
    theme = scrapy.Field()
    score = scrapy.Field()


class MaoYanItem(scrapy.Item):
    title = scrapy.Field()
    star = scrapy.Field()
    rank = scrapy.Field()
    release_time = scrapy.Field()
