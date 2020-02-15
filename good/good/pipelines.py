class GoodPipeline(object):
    def process_item(self, item, spider):
        if spider.name == 'jd':
            print(item)
        return item


class JSPipeline:
    def process_item(self, item, spider):
        if spider.name == 'js':
            print(item)
        return item


class JS1Pipeline:
    def process_item(self, item, spider):
        if spider.name == 'js1':
            print(item)
        return item


class TBPipeline:
    def process_item(self, item, spider):
        if spider.name == 'tb':
            print(item)
        return item


class GZPipeline:
    def process_item(self, item, spider):
        if spider.name == 'gz':
            print(item)
        return item


class ZHPipeline:
    def process_item(self, item, spider):
        if spider.name == 'zh':
            print(item)
        return item

class SNPipeline:
    def process_item(self, item, spider):
        if spider.name == 'suning':
            print(item)
        return item


