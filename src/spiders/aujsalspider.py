import scrapy

class AujsalSpider(scrapy.Spider):
    name = 'aujsal'
    start_urls = ['https://cursos.leon.uia.mx/intercambiovirtual/index.php']

    def parse(self, response):
        for countries in response.css('#accordionExample > .accordion-item'):
            for universities in countries.css('.accordion-collapse > .accordion-body > .accordion > .card'):
                university = universities.css(
                    'h5 > button::text').get().strip()

                for courses in universities.css('table tbody tr'):
                    course = courses.css('td::text').getall()

                    item = {
                        'title': course[1],
                        'type': course[0],
                        'career': course[2],
                        'university': university,
                        'startDate': course[4],
                        'endDate': course[5],
                        'url': courses.css('td a::attr(href)').get()
                    }

                    yield item
