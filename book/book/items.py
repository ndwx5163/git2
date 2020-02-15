import scrapy


class QiDianItem(scrapy.Item):
    href = scrapy.Field()
    name_chapter = scrapy.Field()
    num_chapter = scrapy.Field()
    first_time = scrapy.Field()
    num_character = scrapy.Field()
    content = scrapy.Field()


class ZongHengItem(scrapy.Item):
    href = scrapy.Field()
    name_chapter = scrapy.Field()
    num_chapter = scrapy.Field()
    num_character = scrapy.Field()
    time_update = scrapy.Field()
    content = scrapy.Field()


class DangDangItem(scrapy.Item):
    title = scrapy.Field()
    image = scrapy.Field()
    press = scrapy.Field()
    info = scrapy.Field()
    detail = scrapy.Field()
    current_price = scrapy.Field()
    author = scrapy.Field()
    num_review = scrapy.Field()
