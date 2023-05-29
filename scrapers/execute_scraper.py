import os, sys

# from twisted.internet import reactor
from crochet import setup

from scrapy.utils.project import get_project_settings
from scrapers.scrapers.spiders.indeed_spider import IndeedSpider
from scrapers.scrapers.spiders.jobstreet_spider import JobStreetSpider
from scrapy.crawler import CrawlerRunner

setup()


class Scapers:
    def __init__(self):
        os.environ.setdefault("SCRAPY_SETTINGS_MODULE", "scrapers.scrapers.settings")
        self.runner = CrawlerRunner(get_project_settings())
        self.IndeedSpider = IndeedSpider
        self.JobStreetSpider = JobStreetSpider

    def run_indeed_spider(self, search_query, location, max_pages):
        self.runner.crawl(
            self.IndeedSpider,
            search_query=search_query,
            location=location,
            max_pages=max_pages,
        )

    def run_jobstreetvn_spider(self, search_query, location, max_pages):
        self.runner.crawl(
            self.JobStreetSpider,
            search_query=search_query,
            location=location,
            max_pages=max_pages,
        )

