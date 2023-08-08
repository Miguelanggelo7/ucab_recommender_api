import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.keys import Keys
from time import sleep
from bs4 import BeautifulSoup  # Añadir esta línea para importar BeautifulSoup

class LinkedinSpider(scrapy.Spider):
    name = 'linkedin'
    start_urls = ['https://www.linkedin.com/login']
    profile_url = 'https://www.linkedin.com/in/feredev/'
 
    def __init__(self):
        chrome_options = ChromeOptions()
        chrome_service = ChromeService(executable_path='C:/webDrivers/chromedriver.exe')
        self.driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    def parse(self, response):
        self.driver.get("https://www.linkedin.com/login")
        sleep(2)
        email_input = self.driver.find_element("id", "username")
        password_input = self.driver.find_element("id", "password")
        email_input.send_keys('miguelanggelo21@gmail.com')
        password_input.send_keys('#MIG21uel')
        password_input.send_keys(Keys.RETURN)
        sleep(5)

        # Verificar si el inicio de sesión fue exitoso
        if "feed" in self.driver.current_url:
            self.logger.info("Inicio de sesión exitoso.")
            # Navegar al perfil deseado después del inicio de sesión
            self.driver.get(self.profile_url)
            sleep(5)
            return self.parse_profile(response)  # Procesar el perfil y retornarlo
        else:
            self.logger.error("Inicio de sesión fallido. Verifica tus credenciales.")
        
    def parse_profile(self, response):
        profile_content = self.driver.page_source
        soup = BeautifulSoup(profile_content, 'html.parser')
        
        # Buscar el div con id "about" y verificar si existe
        about_div = soup.find('div', {'id': 'about'})
        if about_div:
            # Extraer el texto del elemento si se encuentra el div "about"
            info_element = soup.find('div', {'class': 'inline-show-more-text inline-show-more-text--is-collapsed inline-show-more-text--is-collapsed-with-line-clamp full-width'})
            information = info_element.get_text(strip=True)
        else:
            # Si no se encontró el div "about", establecer information como una cadena vacía
            information = ""
        
        # Buscar el div con id "experience" y luego obtener el section padre
        experience_div = soup.find('div', {'id': 'experience'})
        if experience_div:
            parent_section = experience_div.find_parent('section')
            # Buscar los elementos que contienen las experiencias dentro del section adecuado
            experiences = []
            if parent_section:
                # Verificar que el span con la clase "visually-hidden" esté dentro del div adecuado
                experience_items = parent_section.select('div.display-flex.align-items-center.mr1.t-bold span.visually-hidden')
                for item in experience_items:
                    experience = item.get_text(strip=True)
                    experiences.append(experience)
        else:
            # Si no se encontró el div con id "experience", establecer experiences como una lista vacía
            experiences = []
        
        # Buscar el div con id "skills" y luego obtener el section padre
        skills_div = soup.find('div', {'id': 'skills'})
        parent_section_skills = skills_div.find_parent('section')

        # Inicializar el array de skills
        skills = []
        if parent_section_skills:
            # Encontrar la etiqueta 'a' para redirigirnos al enlace del href
            skills_link = parent_section_skills.find('a', {'class': 'optional-action-target-wrapper artdeco-button artdeco-button--tertiary artdeco-button--standard artdeco-button--2 artdeco-button--muted inline-flex justify-center full-width align-items-center artdeco-button--fluid'})

            # Verificar si se encontró el enlace y acceder a la nueva página
            if skills_link:
                skills_page_url = skills_link.get('href')
                self.driver.get(skills_page_url)
                sleep(2)

                # Obtener la página con las skills y buscar los elementos que cumplan con la estructura adecuada
                skills_content = self.driver.page_source
                skills_soup = BeautifulSoup(skills_content, 'html.parser')
                skill_items = skills_soup.select('div.display-flex.align-items-center.mr1.hoverable-link-text.t-bold span.visually-hidden')

                # Agregar las skills al array
                for item in skill_items:
                    skill = item.get_text(strip=True)
                    skills.append(skill)

        # Crear el objeto a devolver con la información de experiences y skills
        result = {
            'information': information,
            'experiences': experiences,
            'skills': skills
        }

        return result
        
    def closed(self, reason):
        self.driver.quit()
