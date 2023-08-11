import scrapy
from urllib.parse import urljoin
from src.database.db import db, get_session
from src.models.courses import Course
from src.models.levels import Level
from sqlalchemy import select

class AujsalSpider(scrapy.Spider):
    name = 'aujsal'
    start_urls = ['https://cursos.leon.uia.mx/intercambiovirtual/index.php']
    items = []
    url_set = set()

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

                    if item['url']:
                        self.url_set.add(item['url'])

                    # Almacenar el objeto en la lista self.objetos
                    self.items.append(item)

                    yield item      

    def closed(self, reason):

        session = get_session()

        for item in self.items:

            url = item['url']

            # Verificar si el curso ya existe en la base de datos por su URL
            existing_course = session.query(Course).filter_by(url=url).first()

            if (url in self.url_set) and (existing_course is None):

                self.url_set.remove(url)  # Remover el URL del conjunto para evitar duplicados
                
                course_type = item['type'].lower()  # Convertir a minúsculas

                if "pregrado" in course_type:
                    nameLevel = "pregrado"
                elif "posgrado" in course_type:
                    nameLevel = "posgrado"
                else:
                    nameLevel = "formacion continua"

                statement = select(Level).filter_by(name=nameLevel)
                level = session.scalars(statement).first()

                course = Course(
                    title=item['title'],
                    begin_date=item['startDate'],
                    end_date=item['endDate'],
                    university=item['university'],
                    url=item['url'],
                    career=item['career'],
                    level_id=level.id
                )

                session.add(course)

        session.commit()