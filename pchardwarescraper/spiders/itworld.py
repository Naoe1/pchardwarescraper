import scrapy


class ItworldSpider(scrapy.Spider):
    name = "IT World"
    allowed_domains = ["itworldph.com"]
    start_urls = ["https://itworldph.com/shop/category/processors-62", "https://itworldph.com/shop/category/video-cards-64", "https://itworldph.com/shop/category/motherboards-61", "https://itworldph.com/shop/category/chassis-65", "https://itworldph.com/shop/category/cooling-systems-aircooling-system-92", "https://itworldph.com/shop/category/cooling-systems-aio-liquid-cooling-system-89", "https://itworldph.com/shop/category/memory-modules-57", "https://itworldph.com/shop/category/storage-devices-hard-disk-106", "https://itworldph.com/shop/category/storage-devices-solid-state-drive-72", "https://itworldph.com/shop/category/power-sources-63", "https://bermorzone.com.ph/product-category/cooling-systems/aircooling-system/",  ]

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
