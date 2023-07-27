import os
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from dotenv import load_dotenv
from supabase import create_client, Client
from datetime import datetime

load_dotenv()


def run_all_spiders():
    os.environ['SCRAPY_SETTINGS_MODULE'] = 'pchardwarescraper.settings'

    process = CrawlerProcess(get_project_settings())
    spider_list = ['PC Express', 'EasyPC', 'Dynaquest', 'Techmovers', 'Bermorzone', 'IT World']

    for spider_name in spider_list:
        process.crawl(spider_name)

    process.start()
    save_date()

def save_date():
    url = os.getenv('SUPABASE_URL')
    key = os.getenv('SUPABASE_KEY')
    supabase: Client = create_client(url, key)
    current_date = datetime.now().strftime("%Y-%m-%d")
    supabase.table('last_updated').update({'date_upd': current_date}).eq('id', 1).execute()

if __name__ == '__main__':
    run_all_spiders()
