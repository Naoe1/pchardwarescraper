import scrapy


class DynaquestsSpider(scrapy.Spider):
    name = "Dynaquest"
    allowed_domains = ["dynaquestpc.com"]
    start_urls = ["https://dynaquestpc.com/collections/processor","https://dynaquestpc.com/collections/graphics-card", "https://dynaquestpc.com/collections/motherboard"]
    
    def parse(self, response):
        category = response.url.split("/")[-1].split("?")[0]
        for product in response.css('div.row-container'):
            yield {
                'name': product.css('a.title-5::text').get(),
                'price': product.css('span.price::text').get(),
                'link': "https://dynaquestpc.com" + product.css('a.title-5').attrib['href'],
                'category': category,
                'vendor': "Dynaquest"
            }

        next_page = response.css(
                'div.pagination li.next a::attr(href)').get()
        if next_page is not None and next_page != 'javascript:;':
            next_page_url = "https://dynaquestpc.com" + next_page
            yield response.follow(next_page_url, callback=self.parse)
