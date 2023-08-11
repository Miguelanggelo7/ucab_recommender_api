from src.spiders.emoviespider import EmoviesSpider
from src.spiders.aujsalspider import AujsalSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from src.models.courses import Course
from src.models.levels import Level
from src.database.db import db
from flask import Flask

app = Flask(__name__)

def run_spiders():
    process = CrawlerProcess(get_project_settings())

    # Iniciar las arañas
    process.crawl(EmoviesSpider)
    process.crawl(AujsalSpider)
    process.start()

if __name__ == '__main__':
    from twisted.internet import reactor
    reactor.callWhenRunning(run_spiders)
    reactor.run()
