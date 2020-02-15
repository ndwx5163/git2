import scrapy


class GoodItem(scrapy.Item):

    name = scrapy.Field()
    price = scrapy.Field()
    store = scrapy.Field()
    num_review = scrapy.Field()
    image = scrapy.Field()

class JSItem(scrapy.Item):

    title = scrapy.Field()
    article = scrapy.Field()
    num_diamond = scrapy.Field()
    author = scrapy.Field()
    date = scrapy.Field()
    time = scrapy.Field()
    num_character = scrapy.Field()
    num_read = scrapy.Field()

class GZItem(scrapy.Item):

    title = scrapy.Field()
    image = scrapy.Field()
    info = scrapy.Field()
    price = scrapy.Field()

class ZHItem(scrapy.Item):

    title = scrapy.Field()
    one_review = scrapy.Field()
    num_agree = scrapy.Field()
    num_review = scrapy.Field()


class SuningItem(scrapy.Item):

    title = scrapy.Field()
    num_review = scrapy.Field()
    image = scrapy.Field()
    price = scrapy.Field()
    parameter = scrapy.Field()
    store = scrapy.Field()

