import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem


class ImagePipeline(ImagesPipeline):
    """下载图片使用的特殊管道。"""

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url, meta={"name": item["name"]})

    def file_path(self, request, response=None, info=None):
        return 'full/' + request.meta.get("name") + '.jpg'

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item


class LandscapePipeline:
    def process_item(self, item, spider):
        if spider.name == "landscape":
            print(item)
        return item
