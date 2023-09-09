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

        next_page_url = response.css('li.pages-item-next > a::attr(href)').get()
        if next_page_url is not None:
            yield response.follow(next_page_url, callback=self.parse)

    def parse_watch_page(self, response):
        watch_data = {
            'url': response.url,
            'title': response.css('span.product-item-name::text').get(),
            'sku': response.css('span.product-item-sku::text').get(),
            'currency': response.css('span.price::text').get().split('$')[0],
            'price': response.css('span.price::text').get().split('$ ')[1].replace(',', ''),
            'watch_spec': {}
        }
        table_cols = response.css('.tbw-row > .cols')
        for table_col in table_cols:
            col_subtitle = table_col.css('.table-title::text').get().strip('\n').strip()
            subtables = table_col.css('ul.table > li')
            for subtable in subtables:
                subtable_label = subtable.css('.table__label::text').get().strip('\n').strip()
                subtable_value = subtable.css('.table__context::text').get().strip('\n').strip()
                # watch_data['watch_spec'][col_subtitle][subtable.css('.table__label::text').get()] = subtable.css('.table__context::text').get()
                watch_data.setdefault('watch_spec', {}).setdefault(col_subtitle, {}).setdefault(subtable_label, subtable_value)
        yield watch_data
