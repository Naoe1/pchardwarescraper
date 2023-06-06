import scrapy
import re
import math

class TechmoversSpider(scrapy.Spider):
    name = "techmovers"
    allowed_domains = ["www.techmoversph.com"]
    start_urls = ["https://www.techmoversph.com/Processors-c82748371", "https://www.techmoversph.com/Graphics-Cards-c83585010", "https://www.techmoversph.com/Motherboards-c143943026"]
    
    def parse(self, response):
        category = response.url.split("/")[-1].split("?")[0].split("-")[0]
        for product in response.css('.grid-product__wrap-inner'):
            yield {
                'name': product.css('.grid-product__title-inner::text').get(),
                'price': product.css('.grid-product__price-value::text').get(),
                'link': product.css('.grid-product__title').attrib['href'],
                'category': category,
                'vendor': 'Techmovers',
            }
        
        if response.css('.ec-footer').get() is not None:
            current_offset = 0
            product_count = int(re.search(r'(\d+) items', response.css('.pager__count-pages::text').get()).group(1))
            max_page = math.floor(product_count/60)*60
            if "offset" in response.url:
                current_offset = int(response.url.split('=')[-1])
            if current_offset < max_page:
                next_offset = current_offset + 60
                current_url = response.url.split('?')[0] + f"?offset={next_offset}"
                yield response.follow(current_url, callback=self.parse)
