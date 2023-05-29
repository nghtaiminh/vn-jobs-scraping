import scrapy
import urllib
import json
from datetime import datetime

from scrapy.exceptions import CloseSpider


class JobStreetSpider(scrapy.Spider):
    name = "jobstreet_spider"
    base_url = "https://www.jobstreet.vn"
    job_page_url = (
        "https://www.jobstreet.vn/job/"  
    )


    def __init__(self, search_query="Data Intern", location="Ho Chi Minh", max_pages=2):
        self.search_query = urllib.parse.quote(search_query)
        self.location = urllib.parse.quote(location)
        self.max_pages = max_pages
        self.count = 0
        # https://www.jobstreet.vn/j?sp=search&q=intern&l=Ho+Chi+Minh
        self.start_urls = [
            self.base_url + "/j?sp=" + self.search_query + "&l=" + self.location
        ]
        print("start_urls: ", self.start_urls)

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], callback=self.parse)

    def parse(self, response):

        if self.count >= self.max_pages:
            raise CloseSpider("Reached max pages")

        for job in response.css("div.job-card"):
            # job id from data-job-id class
            job_id = job.css("button::attr(data-job-id)").get()
            print("job_id: ", job_id)
            job_title = job.css("h3.job-title > a::text").extract_first()
            print(job_title)

            yield scrapy.Request(
                url=f"{self.job_page_url}-{job_id}",
                callback=self.parse_job_details,
                meta={
                    "job_id": job_id,
                    "job_title": job_title,
                    "link": f"{self.job_page_url}-{job_id}",
                },
            )

        # get the next page url
        next_page = response.css("a.next-page-button::attr(href)").extract_first()
        if next_page is not None and self.count < self.max_pages:
            next_page = response.urljoin(next_page)
            self.count += 1
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_job_details(self, response):

        # the data is brought from the previous reponse
        job_id = response.meta["job_id"]
        job_title = response.meta["job_title"]
        link = response.meta["link"]

        # scrape information from the job page
        # get comapany span element with company class name
        company_name = response.css("span.company::text").extract_first()
        # get job description from div with job-description-container id
        job_description = response.css("div#job-description-container ::text").getall()
        print
        # get job location from span with location class name
        job_location = response.css("span.location::text").extract_first()
        # get listed date from span with listed_date class name
        listed_date = response.css("span.listed-date::text").extract_first()
        # get apply link from a with apply-button class name
        apply_link = response.css("a.apply-button::attr(href)").extract_first()
        # yield the data
        yield {
            "job_id": job_id,
            "job_title": job_title,
            "company_name": company_name,
            "job_description": job_description,
            "job_location": job_location,
            "listed_date": listed_date,
            "apply_link": self.base_url +  apply_link,
            "job_link": link,
            "scraped_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
