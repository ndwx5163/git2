import scrapy


class ImageItem(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()


class FileItem(scrapy.Item):
    file_urls = scrapy.Field()
    files = scrapy.Field()


class LandscapeItem(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()
    name = scrapy.Field()
    image_paths = scrapy.Field()
