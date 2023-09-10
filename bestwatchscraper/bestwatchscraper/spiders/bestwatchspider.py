import scrapy
from bestwatchscraper.items import WatchItem, WatchSpecItem, WatchSpecInfoItem, WatchSpecDialItem, WatchSpecCaseItem, \
    WatchSpecBandItem, WatchSpecMovementItem, WatchSpecFeatureItem


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
        watch_item = WatchItem()
        watch_item['url'] = response.url
        watch_item['title'] = response.css('span.product-item-name::text').get()
        watch_item['sku'] = response.css('span.product-item-sku::text').get()
        watch_item['currency'] = response.css('span.price::text').get().split('$')[0]
        watch_item['price'] = response.css('span.price::text').get().split('$ ')[1].replace(',', '')
        watch_item['watch_spec'] = WatchSpecItem()

        # watch_spec_data = {}

        # watch_data = {
        #     'url': response.url,
        #     'title': response.css('span.product-item-name::text').get(),
        #     'sku': response.css('span.product-item-sku::text').get(),
        #     'currency': response.css('span.price::text').get().split('$')[0],
        #     'price': response.css('span.price::text').get().split('$ ')[1].replace(',', ''),
        #     'watch_spec': {}
        # }
        table_cols = response.css('.tbw-row > .cols')
        for table_col in table_cols:
            col_subtitle = table_col.css('.table-title::text').get().strip('\n').strip().lower()
            watch_spec_category = WatchSpecItem

            match col_subtitle:
                case 'information':
                    watch_item['watch_spec'][col_subtitle] = WatchSpecInfoItem()
                case 'dial':
                    watch_item['watch_spec'][col_subtitle] = WatchSpecDialItem()
                case 'case':
                    watch_item['watch_spec'][col_subtitle] = WatchSpecCaseItem()
                case 'band':
                    watch_item['watch_spec'][col_subtitle] = WatchSpecBandItem()
                case 'movement':
                    watch_item['watch_spec'][col_subtitle] = WatchSpecMovementItem()
                case 'features':
                    watch_item['watch_spec'][col_subtitle] = WatchSpecFeatureItem()

            # watch_item['watch_spec'][col_subtitle] = watch_spec_item
            subtables = table_col.css('ul.table > li')
            for subtable in subtables:
                subtable_label = subtable.css('.table__label::text').get().strip('\n').strip().lower().replace(' ', '_')
                subtable_value = subtable.css('.table__context::text').get().strip('\n').strip()
                watch_item['watch_spec'][col_subtitle][subtable_label] = subtable_value
                # watch_data['watch_spec'][col_subtitle][subtable.css('.table__label::text').get()] = subtable.css('.table__context::text').get()
                # watch_spec_data.setdefault(col_subtitle, {}).setdefault(subtable_label, subtable_value)
                # watch_spec_item = subtable_value

        # watch_item['watch_spec'] = watch_spec_item

        yield watch_item
