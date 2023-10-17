import scrapy
from urllib.parse import urljoin
from src.database.db import db, get_session
from src.models.courses import Course
from src.models.levels import Level
from sqlalchemy import select


class EmoviesSpider(scrapy.Spider):
    name = 'emovies'
    start_urls = ['https://emovies.oui-iohe.org/nuestros-cursos/']
    objetos = []  # Define the attribute
    url_set = set()

    def parse(self, response):
        # Obtener los elementos div.course__inner de la página actual
        div_elements = response.xpath(
            '//div[contains(@class, "course__inner")]')

        for div_element in div_elements:
            try:
                # Obtener el título
                titulo = div_element.xpath('.//h3/text()').get()

                # Obtener los elementos div.details__item dentro del div.course__inner
                details_elements = div_element.xpath(
                    './/div[contains(@class, "details__item")]')

                # Inicializar variables para los campos de información
                university = ""
                career = ""
                tipo = ""
                startDate = ""
                endDate = ""
                url = ""

                # Iterar sobre los elementos div.details__item
                for details_element in details_elements:
                    # Obtener el texto dentro de la etiqueta strong
                    strong_text = details_element.xpath(
                        './/sup[@class="light"]/text()').get()
                    text = details_element.xpath(
                        'normalize-space(string(.//strong))').get()

                    # Identificar el campo y asignar el valor correspondiente
                    if "IES / HEI" in strong_text:
                        university = text
                    elif "Programa académico / Academic Program" in strong_text:
                        career = text
                    elif "Nivel des programa / Program Level" in strong_text:
                        tipo = text
                    elif "Fecha de inicio curso / Course start date" in strong_text:
                        startDate = text.strip()
                    elif "Fecha de terminación / Course finish date" in strong_text:
                        endDate = text.strip()

                # Obtener el href de la etiqueta a.button--white
                url = div_element.css('a.button--white::attr(href)').get()

                if url:
                    self.url_set.add(url)


                # Crear el objeto con la información
                objeto = {
                    "title": titulo,
                    "type": tipo,
                    "career": career,
                    "university": university,
                    "startDate": startDate,
                    "endDate": endDate,
                    "url": url
                }

                # Construir la URL completa del curso
                absolute_url = urljoin(response.url, url)

                # Realizar una solicitud a la URL del curso
                yield scrapy.Request(absolute_url, callback=self.parse_requirements, meta={'objeto': objeto})
            except:
                pass

        # Obtener el enlace de la siguiente página
        next_page = response.css('a.next::attr(href)').get()

        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_requirements(self, response):
        # Obtener todos los elementos dentro del div.contents dentro del div#acc-1
        content_elements = response.css('div#acc-1 div.contents *').getall()

        # Concatenar y limpiar el texto de todos los elementos
        requirements = ' '.join(response.xpath(
            '//div[@id="acc-1"]/div[contains(@class, "contents")]//text()').getall()).strip()

        # Obtener el contenido dentro del div de descripción del curso
        description_elements = response.xpath('//div[@class="text"]/node()')

        # Concatenar y limpiar el texto de todos los elementos
        description = ' '.join(
            description_elements.xpath('string()').getall()).strip()
        
        if description.startswith("Descripción del curso"):
            # Eliminar la subcadena "Descripción del curso" del principio de la descripción
            description = description.replace("Descripción del curso", "", 1).strip()

        # Lista de valores que se considerarán como nulos
        null_values = ["Ninguno", "N/A", "Ementa:", "No aplica", "", "–", "NA", ".", "No requiere", "N / A", "n/a", "No", "N.A", "Ninguna", "Ementa: "]

        # Asignar None si description está en la lista de valores nulos, de lo contrario, asignar el valor actual
        description = None if description in null_values else description

        # Asignar None si requirements está en la lista de valores nulos, de lo contrario, asignar el valor actual
        requirements = None if requirements in null_values else requirements


        # Obtener el objeto de la respuesta original
        objeto = response.meta['objeto']

        # Agregar los requisitos y descripcion al objeto
        objeto['requirements'] = requirements
        objeto['description'] = description

        # Almacenar el objeto en la lista self.objetos
        self.objetos.append(objeto)

        yield objeto

    def closed(self, reason):

        session = get_session()

        for objeto in self.objetos:

            url = objeto['url']

            # Verificar si el curso ya existe en la base de datos por su URL
            existing_course = session.query(Course).filter_by(url=url).first()

            if (url in self.url_set) and (existing_course is None):

                self.url_set.remove(url)  # Remover el URL del conjunto para evitar duplicados

                course_type = objeto['type'].lower()  # Convertir a minúsculas

                if "pregrado" in course_type:
                    nameLevel = "pregrado"
                elif "posgrado" in course_type:
                    nameLevel = "posgrado"
                else:
                    nameLevel = "formacion continua"

                statement = select(Level).filter_by(name=nameLevel)
                level = session.scalars(statement).first()

                course = Course(
                    title=objeto['title'],
                    begin_date=objeto['startDate'],
                    end_date=objeto['endDate'],
                    university=objeto['university'],
                    url=objeto['url'],
                    career=objeto['career'],
                    level_id=level.id,
                    requirements=objeto['requirements'],
                    description=objeto['description']
                )

                session.add(course)

        session.commit()