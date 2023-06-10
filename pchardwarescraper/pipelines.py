# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import re
from itemadapter import ItemAdapter
from pchardwarescraper.utils.categorymap import categories
from dotenv import load_dotenv
from supabase import create_client, Client
import os

load_dotenv()
class PchardwarescraperPipeline:
    def process_item(self, item, spider):
        if spider.name != 'mobo':
            adapter = ItemAdapter(item)
            field_names = adapter.field_names()
            for field_name in field_names:
                adapter[field_name] = adapter.get(field_name).strip()
            
            adapter['price'] = self.clean_and_convert_value(adapter.get('price'))
            adapter['category'] = categories.get(adapter.get('category'))

        
        return item
    
    def clean_and_convert_value(self, value):
        # Remove non-numeric characters
        cleaned_value = re.sub(r'[^0-9.]', '', value)
        float_value = float(cleaned_value)
        decimal_value = round(float_value, 2)

        return decimal_value

class SupabasePipeline:
    def __init__(self):
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv("SUPABASE_KEY")
    
    def open_spider(self, spider):
        self.client: Client = create_client(self.supabase_url,self.supabase_key)

    def trim_prod_name(self, product_name, word_length):
        prod_arr = product_name.split()
        trimmed_word = ' '.join(prod_arr[:word_length])
        return trimmed_word

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        category = adapter['category']
        name = adapter['name']
        link = adapter['link']
        price = adapter['price']
        vendor = adapter['vendor']
        if category == 'Processor':
            brand = name.split(" ")[0].replace("®", "")
            trimmed_name = self.trim_prod_name(name, 5)
            resp = self.client.rpc("search_processor_similarity", params={'p_brand': brand, 'p_model_name': trimmed_name}).execute()
            data = resp.data
            if not data:
                self.client.table("no_match_products").insert({"name": name, "category": category, "link": link,'price': price}).execute()
            else:
                self.client.table("vendor_processor").insert({"vendor_id":vendor, "component_id": resp.data[0]['full_name'], "price": price, "link": link, "title": name}).execute()
        elif category == 'Motherboard':
            brand = name.split(" ")[0].replace("®", "")
            trimmed_name = self.trim_prod_name(name, 7)
            resp = self.client.rpc("search_motherboard_similarity", params={'p_brand': brand, 'p_model_name': trimmed_name}).execute()
            data = resp.data
            if not data:
                self.client.table("no_match_products").insert({"name": name, "category": category, "link": link,'price': price}).execute()
            else:
                self.client.table("vendor_motherboard").insert({"vendor_id":vendor, "component_id": resp.data[0]['full_name'], "price": price, "link": link, "title": name}).execute()

        return item
            


    