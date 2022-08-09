# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import JsonItemExporter

class ScrapersPipeline:
    def open_spider(self, spider):
        if spider.name == 'indeed_spider':
            self.file = open('scrapers/scrapers/data/indeed_jobs.json', 'wb')
        elif spider.name == 'jobstreet_spider':
            self.file = open('scrapers/scrapers/data/jobstreet_jobs.json', 'wb')

        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
