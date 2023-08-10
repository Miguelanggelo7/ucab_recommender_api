from src.spiders.emoviespider import EmoviesSpider
from src.spiders.aujsalspider import AujsalSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from src.models.courses import Course
from src.models.levels import Level
from src.database.db import db
from flask import Flask

app = Flask(__name__)

def get_new_courses(emovies_results, aujsal_results):
    new_courses = []

    # Obtener resultados de las arañas
    new_courses.extend(emovies_results)
    new_courses.extend(aujsal_results)

    return new_courses

def run_spiders_and_get_results():
    process = CrawlerProcess(get_project_settings())

    # Crear listas para almacenar los resultados
    emovies_results = []
    aujsal_results = []

    def collect_results(item, spider_name):
        if spider_name == "emovies":
            emovies_results.append(item)
        elif spider_name == "aujsal":
            aujsal_results.append(item)

    # Iniciar las arañas
    process.crawl(EmoviesSpider, callback=lambda item: collect_results(item, "emovies"))
    process.crawl(AujsalSpider, callback=lambda item: collect_results(item, "aujsal"))
    process.start()

    return emovies_results, aujsal_results

def run_spiders():
    # Obtener resultados de las arañas
    emovies_results, aujsal_results = run_spiders_and_get_results()

    # Obtener los cursos nuevos
    new_courses = get_new_courses(emovies_results, aujsal_results)

    # # Agregar los cursos nuevos a la base de datos
    # existing_courses = Course.query.all()

    # for new_course in new_courses:
    #     existing_course = next((course for course in existing_courses if course.title == new_course['title']), None)

    #     if not existing_course:
    #         course = Course(
    #             title=new_course['title'],
    #             begin_date=new_course['startDate'],
    #             end_date=new_course['endDate'],
    #             university=new_course['university'],
    #             requirements=new_course['requirements']
    #         )

    #         # Determinar level_id basado en el tipo de curso
    #         if 'Pregrado' in new_course['type']:
    #             level_id = 1
    #         elif 'Postgrado' in new_course['type']:
    #             level_id = 2
    #         else:
    #             level_id = 3

    #         level = Level.query.get(level_id)
    #         if level:
    #             course.level = level

    #         db.session.add(course)

    # db.session.commit()
    print("EMPEZAMOSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS", flush=True)
    print(new_courses, flush=True)
    print("TERMINAMOSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS", flush=True)

if __name__ == '__main__':
    run_spiders()
