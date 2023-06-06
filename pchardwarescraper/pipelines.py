# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import re
from itemadapter import ItemAdapter
from pchardwarescraper.utils.categorymap import categories

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
