import scrapy

# NOTE: This script is written in 01/08/2022.
# I am not sure if it will work in the future.

class IndeedSpider(scrapy.Spider):
    name= 'indeed_spider'
    base_url = 'https://vn.indeed.com'
    job_page_url = 'https://www.indeed.com/viewjob?jk='

    def start_requests(self):
        # The start URL is tested with parameters:
        # q = Data Intern
        # l = Ho Chi Minh City

        start_urls = ["https://vn.indeed.com/m/jobs?q=data+intern&l=Ho+Chi+Minh+City"]
        yield scrapy.Request(start_urls[0], callback=self.parse)

    def parse(self, response):
        for job in response.css('div.job_seen_beacon'):
            job_id = job.css('h2.jobTitle > a::attr(data-jk)').extract_first()
            location = job.css('div.companyLocation ::text').extract_first()

            yield scrapy.Request(url=self.job_page_url + job_id, 
                                callback=self.parse_job_details,
                                meta={'link': self.job_page_url + job_id,
                                    'location': location})

        # get the next page url
        next_page = response.xpath('//a[@aria-label="Next"]/@href').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)


    def parse_job_details(self, reponse):
        # the url is brought from the previous reponse
        link = reponse.meta['link']
        location = reponse.meta['location']
        # scrape information from the job page
        job_title = reponse.css('h1.jobsearch-JobInfoHeader-title::text').extract_first()
        company_name = reponse.css('div.jobsearch-InlineCompanyRating a::text').extract_first()
        rating = reponse.xpath('//meta[@itemprop="ratingValue"]/@content').extract_first()
        review_count = reponse.xpath('//meta[@itemprop="ratingCount"]/@content').extract_first()
        job_description = reponse.css('div#jobDescriptionText ::text').getall()

        try:
            salary_range = reponse.css('div.metadata.salary-snippet-container ::text').extract_first()
        except:
            salary_range = None

        yield {
            'link': link,
            'title': job_title,
            'company': company_name,
            'location': location,
            'salary': salary_range,
            'rating': rating,
            'review_count': review_count,
            'description': ' '.join(job_description).strip().replace('\n', ''),
        }






