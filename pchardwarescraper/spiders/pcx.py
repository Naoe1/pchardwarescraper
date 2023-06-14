import scrapy


class PcxSpider(scrapy.Spider):
    name = "PC Express"
    allowed_domains = ["pcx.com.ph"]
    start_urls = ["https://pcx.com.ph/product-category/components/processor/", "https://pcx.com.ph/product-category/components/motherboards/", "https://pcx.com.ph/product-category/components/graphics-card/"]

    def parse(self, response):
        category = response.url.split("/")[5]
        for product in response.css('.product-grid-item'):
            yield {
                'name': product.css('.product-title a::text').get(),
                'price': product.css('span.woocommerce-Price-amount::text').get(),
                'link': product.css('.product-title a').attrib['href'],
                'category': category,
                'vendor': 'PC Express',
            }

        next_page = response.css('a.next::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
