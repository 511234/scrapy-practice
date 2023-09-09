import scrapy
import json

class StrataspiderSpider(scrapy.Spider):
    name = 'strataspider'
    allowed_domains = ['strata.ca']
    start_urls = ['http://strata.ca/']

    def start_requests(self):
        url = "https://strata.ca/toronto/homes-for-rent?center=%5B43.6657%2C-79.3856%5D&ownershipPreference=RENT&zoom=13"
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        listings = json.loads(response.text)
        for listing in listings:
            yield {
                'name': listing
            }
