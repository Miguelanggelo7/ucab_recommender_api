from src.spiders.emoviespider import EmoviesSpider
from src.spiders.aujsalspider import AujsalSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

def run_spiders():
    process = CrawlerProcess(get_project_settings())
    process.crawl(EmoviesSpider)
    process.crawl(AujsalSpider)
    process.start()