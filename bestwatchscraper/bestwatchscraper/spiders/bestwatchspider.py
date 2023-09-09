import re
import scrapy


class BestwatchspiderSpider(scrapy.Spider):
    name = 'bestwatchspider'
    allowed_domains = ['bestwatch.com.hk']
    # start_urls = ['http://bestwatch.com.hk/']

    def start_requests(self):
        url = 'https://bestwatch.com.hk/sale.html'
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        watches = response.css('.product-items .product-item')
        for watch in watches:
            watch_url = watch.css('.product-item-brand a ::attr(href)').get()
            yield response.follow(watch_url, callback=self.parse_watch_page)

    def parse_watch_page(self, response):
        yield {
            'url': response.url,
            'title': response.css('span.product-item-name::text').get(),
            'sku': response.css('span.product-item-sku::text').get(),
            'currency': response.css('span.price::text').get().split('$')[0],
            'price': response.css('span.price::text').get().split('$ ')[1].replace(',', '')
        }
