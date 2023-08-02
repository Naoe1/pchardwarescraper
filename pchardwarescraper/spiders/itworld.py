import scrapy


class ItworldSpider(scrapy.Spider):
    name = "IT World"
    allowed_domains = ["itworldph.com"]
    start_urls = ["https://itworldph.com/shop/category/processor-137", "https://itworldph.com/shop/category/video-card-gpu-123", "https://itworldph.com/shop/category/motherboard-152", "https://itworldph.com/shop/category/chassis-116", "https://itworldph.com/shop/category/cpu-coolers-air-cooling-197","https://itworldph.com/shop/category/cpu-coolers-liquid-cooling-174", "https://itworldph.com/shop/category/memory-130", "https://itworldph.com/shop/category/storage-device-internal-ssd-solid-state-drives-127", "https://itworldph.com/shop/category/storage-device-internal-hdd-hard-drives-234", "https://itworldph.com/shop/category/power-supply-144"  ]
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
        next_page = pagination[-1].attrib['href']
        if next_page is not None and pagination != [] and next_page != '':
            next_page_url = "https://itworldph.com" + next_page
            yield response.follow(next_page_url, callback=self.parse)
