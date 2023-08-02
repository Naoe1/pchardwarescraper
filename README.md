# PC Component Scraper
This project is a web scraper designed to gather the prices from some of the most popular online stores in the Philippines that sell PC components.
## Supported Vendors
The scraper currently supports the following online stores:

* Bermorzone: https://bermorzone.com.ph/
* Dynaquest PC: https://dynaquestpc.com/
* Easy PC: https://easypc.com.ph/
* IT World: https://itworldph.com/
* PC Express: https://pcx.com.ph/
* Techmovers: https://www.techmoversph.com/

## Installation
1. Clone the project repository from GitHub to your local machine and install the required dependencies.
```shell
git clone https://github.com/Naoe1/pchardwarescraper.git
pip install -r requirements.txt
```
2. (Optional) Set up a PostgreSQL database with [Supabase](https://supabase.com/) and create a .env file in the project root directory with your credentials for storage:
```shell
SUPABASE_URL='<url>'
SUPABASE_KEY='<key>'
```

## Usage
If used without Supabase, comment out out SupabasePipeline from `settings.py`
```python
ITEM_PIPELINES = {
   "pchardwarescraper.pipelines.PchardwarescraperPipeline": 300,
   # "pchardwarescraper.pipelines.SupabasePipeline": 400,
}
```
### Run a spider with crawl command
```shell
scrapy crawl <spider_name>
```
### Output scraped items to a file
```shell
scrapy crawl <spider_name> -o output.csv
```

## Data output
Example json output:
```json
{
    "name": "Intel i7-13700K",
    "price": "24027.65",
    "category": "Processor",
    "vendor": "Vendor x",
    "link": "https://www.vendorx.ph/cpus/example-cpu-model"
}
```
