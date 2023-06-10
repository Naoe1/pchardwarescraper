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

    def search_component_similarity(self, category, brand, trimmed_name):
        category = category.replace(' ', '_')
        rpc_name = f'search_{category.lower()}_similarity'
        params = {'p_brand': brand, 'p_model_name': trimmed_name}
        resp = self.client.rpc(rpc_name, params=params).execute()
        return resp.data if resp.data else None

    def insert_no_match_product(self, name, category, link, price):
        self.client.table('no_match_products').insert({
            'name': name,
            'category': category,
            'link': link,
            'price': price
        }).execute()

    def insert_vendor_component(self, vendor, category, component_id, price, link, title):
        category = category.replace(' ', '_')
        table_name = f'vendor_{category.lower()}'
        self.client.table(table_name).insert({
            'vendor_id': vendor,
            'component_id': component_id,
            'price': price,
            'link': link,
            'title': title
        }).execute()

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
            data = self.search_component_similarity(category, brand, trimmed_name)
            if not data:
                self.insert_no_match_product(name, category, link, price)
            else:
                self.insert_vendor_component(vendor, category, data[0]['full_name'], price, link, name)
        elif category == 'Motherboard':
            brand = name.split(" ")[0].replace("®", "")
            trimmed_name = self.trim_prod_name(name, 7)
            data = self.search_component_similarity(category, brand, trimmed_name)
            if not data:
                self.insert_no_match_product(name, category, link, price)
            else:
                self.insert_vendor_component(vendor, category, data[0]['full_name'], price, link, name)
        elif category =='Video card':
            brand = name.split(" ")[0].replace("®", "")
            data = self.search_component_similarity(category, brand, name)
            if not data:
                self.insert_no_match_product(name, category, link, price)
            else:
                self.insert_vendor_component(vendor, category, data[0]['full_name'], price, link, name)
        return item
            


    