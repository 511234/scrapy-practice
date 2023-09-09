import scrapy

class BookspiderSpider(scrapy.Spider):
    name = 'bookspider'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        books = response.css('article.product_pod')
        for book in books:
            relative_url = book.css('h3 a ::attr(href)').get()

            # yield {
            #     'name': book.css('h3 a::text').get(),
            #     'price': book.css('.product_price .price_color::text').get(),
            #     'url': book.css('h3 a').attrib['href']
            # }

        # next_page =  response.css('li.next a ::attr(href)').get()

        if relative_url is not None:
            if 'catalogue/' in relative_url:
                book_url = 'https://books.toscrape.com/' + relative_url
            else:
                book_url = 'https://books.toscrape.com/catalogue/' + relative_url
            yield response.follow(book_url, callback=self.parse_book_page)

    def parse_book_page(self, response):
        table_rows = response.css("table tr")
        yield {
            'url': response.url,
            'title': response.css('.product_main h1::text').get(),
            'product_type': table_rows[1].css('td ::text').get(),
            'price_excl_tax': table_rows[2].css('td ::text').get(),
            'price_incl_tax': table_rows[3].css('td ::text').get(),
            'tax': table_rows[4].css('td ::text').get()
        }