import scrapy


class ItworldSpider(scrapy.Spider):
    name = "IT World"
    allowed_domains = ["itworldph.com"]
    start_urls = ["https://itworldph.com/shop/category/processors-62", "https://itworldph.com/shop/category/video-cards-64", "https://itworldph.com/shop/category/motherboards-61", ]

    def parse(self, response):
        category = response.url.split("/")[5]
        for product in response.css('.o_wsale_product_information_text'):
            yield {
                'name': product.css('h6.o_wsale_products_item_title a::text').get(),
                'price': product.css('.product_price span.oe_currency_value::text').get(),
                'link': "https://itworldph.com" + product.css('h6.o_wsale_products_item_title a').attrib['href'],
                'category': category,
                'vendor': 'IT World'
            }
        
        pagination = response.css('ul.pagination li a')
        if pagination is not None and pagination != []:
            next_page = pagination[-1].attrib['href']
            next_page_url = "https://itworldph.com" + next_page
            yield response.follow(next_page_url, callback=self.parse)
