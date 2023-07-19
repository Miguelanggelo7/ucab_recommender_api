import scrapy


class LinkedinSpider(scrapy.Spider):
    name = "linkedin"
    start_urls = ["https://www.linkedin.com/in/feredev/"]

    def __init__(self, start_urls=None, *args, **kwargs):
        super(LinkedinSpider, self).__init__(*args, **kwargs)
        self.start_urls = start_urls

    def parse(self, response):
        # Extraer habilidades
        habilidades = response.css(
            "div.pv-skill-categories-section ol > li").css("span::text").getall()

        # Extraer experiencias
        experiencias = response.css(
            "section.pv-profile-section.experience-section ul > li").getall()

        # Imprimir los datos extraídos
        print("sdsadsadsa")
        print("Habilidades:", habilidades)
        print("Experiencias:", experiencias)
        yield {"HOLA": "OLA"}

    def closed():
        print("CERRADO")
