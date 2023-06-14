import scrapy


class BermorzoneSpider(scrapy.Spider):
    name = "Bermorzone"
    allowed_domains = ["bermorzone.com.ph"]
    start_urls = ["https://bermorzone.com.ph/product-category/processors/", "https://bermorzone.com.ph/product-category/video-cards/", "https://bermorzone.com.ph/product-category/motherboard/amd-motherboards/", "https://bermorzone.com.ph/product-category/motherboard/intel-motherboards/"]

    def parse(self, response):
        category = response.url.split("/")[4]
        for product in response.css('div.product-item__inner') :
            yield {
                'name': product.css('h2.woocommerce-loop-product__title::text').get(),
                'price': product.css('span.woocommerce-Price-amount > bdi::text').get(),
                'link': product.css('a.woocommerce-LoopProduct-link').attrib['href'],
                'category': category,
                'vendor': 'Bermorzone',
            }

        next_page = response.css('a.next.page-numbers::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
