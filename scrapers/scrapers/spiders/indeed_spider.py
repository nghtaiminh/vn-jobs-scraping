import scrapy
import urllib
from datetime import datetime

from scrapy.exceptions import CloseSpider

# NOTE: This script is written in 01/08/2022.
# I am not sure if it will work in the future.


class IndeedSpider(scrapy.Spider):
    name = "indeed_spider"
    base_url = "https://vn.indeed.com"
    job_page_url = "https://www.indeed.com/viewjob?jk="

    def __init__(self, search_query="Data Intern", location="Ho Chi Minh", max_pages=2):
        self.search_query = urllib.parse.quote(search_query)
        self.location = urllib.parse.quote(location)
        self.max_pages = max_pages
        self.count = 0

        self.start_urls = [
            self.base_url + "/jobs?q=" + self.search_query + "&l=" + self.location
        ]

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], callback=self.parse)

    def parse(self, response):
        # comment the next 2 lines to scrape all the page of the search result
        if self.count >= self.max_pages:
            raise CloseSpider("Reached max pages")

        for job in response.css("div.job_seen_beacon"):
            job_id = job.css("h2.jobTitle > a::attr(data-jk)").extract_first()
            location = job.css("div.companyLocation ::text").extract_first()

            yield scrapy.Request(
                url=self.job_page_url + job_id,
                callback=self.parse_job_details,
                meta={
                    "job_id": job_id,
                    "link": self.job_page_url + job_id,
                    "location": location,
                },
            )

        # get the next page url
        next_page = response.xpath('//a[@aria-label="Next"]/@href').extract_first()
        if next_page is not None and self.count < self.max_pages:
            next_page = response.urljoin(next_page)
            self.count += 1
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_job_details(self, response):

        # the url is brought from the previous reponse
        job_id = response.meta["job_id"]
        link = response.meta["link"]
        location = response.meta["location"]
        # scrape information from the job page
        job_title = response.css(
            "h1.jobsearch-JobInfoHeader-title::text"
        ).extract_first()
        company_name = response.css(
            "div.jobsearch-InlineCompanyRating a::text"
        ).extract_first()
        job_type = response.xpath(
            "*//div[contains(text(), 'Job Type')]/following::div[1]/text()"
        ).extract_first()
        rating = response.xpath(
            '//meta[@itemprop="ratingValue"]/@content'
        ).extract_first()
        review_count = response.xpath(
            '//meta[@itemprop="ratingCount"]/@content'
        ).extract_first()
        job_description = response.css("div#jobDescriptionText ::text").getall()
        date_posted = response.css(
            "div.jobsearch-JobMetadataFooter > div:nth-of-type(2)::text"
        ).extract_first()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            salary_range = response.xpath(
                '//div[contains(text(), "Salary")]/following::span[1]/text()'
            ).extract_first()
        except:
            salary_range = None

        try:
            company_link = response.css(
                "div.jobsearch-InlineCompanyRating a::attr(href)"
            ).extract_first()
        except:
            company_link = None

        yield {
            "job_id": job_id,
            "link": link,
            "title": job_title,
            "job_type": job_type,
            "company": company_name,
            "company_link": company_link,
            "location": location,
            "salary": salary_range,
            "rating": rating,
            "review_count": review_count,
            "description": " ".join(job_description).strip().replace("\n", ""),
            "date_posted": date_posted,
            "timestamp": timestamp,
        }
