import scrapy
import json

class EasypcSpider(scrapy.Spider):
    name = "EasyPC"
    allowed_domains = ["https://easypc.com.ph"]
    start_urls = ["https://easypc.com.ph/collections/processor-amd/products.json?limit=250", "https://easypc.com.ph/collections/processor-intel/products.json?limit=250", "https://easypc.com.ph/collections/motherboard/products.json?limit=250", "https://easypc.com.ph/collections/graphic-card/products.json?limit=250", "https://easypc.com.ph/collections/cpu-cooling/products.json?limit=250", "https://easypc.com.ph/collections/pc-case/products.json?limit=250", "https://easypc.com.ph/collections/power-supply/products.json?limit=250", "https://easypc.com.ph/collections/hard-disk/products.json?limit=250", "https://easypc.com.ph/collections/memory/products.json?limit=250", "https://easypc.com.ph/collections/solid-state-drive/products.json?limit=250"]
    
    def parse(self, response):
        products = json.loads(response.text)['products']
        category = response.url.split("/")[-2].split("-")[0]
        for product in products:
            in_Stock = product['variants'][0]['available']
            if in_Stock:
                yield {
                    'name': product['title'],
                    'price': product['variants'][0]['price'],
                    'link': "https://easypc.com.ph/pages/search-results-page?q=" + product['title'].replace(" ","%20"),
                    'category': category,
                    'vendor': "EasyPC"
                }


