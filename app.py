from flask import Flask
from flask_migrate import Migrate
from src.database.db import db
from src.models.courses import Course
from src.models.levels import Level
from src.models.user_academic_records import UserAcademicRecord
from src.models.users import User
from src.routes.auth import auth_blueprint
from src.models.skills import Skill
from src.models.user_skills import UserSkill
from src.models.user_specializations import UserSpecialization
from src.models.user_preferences import UserPreference
from models.specializations import Specialization

import subprocess
from flask_cors import CORS

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from src.tasks.my_cron import run_spiders
from apscheduler.schedulers.twisted import TwistedScheduler
from scrapy import spiderloader
from scrapy.utils import project
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor, defer
from scrapy.utils.log import configure_logging

configure_logging()
scheduler = TwistedScheduler()
scheduler.add_job(run_spiders, 'interval', days=1)
scheduler.start()
reactor.run()

# Configura tu variable DATABASE_URL aquí directamente
DATABASE_URL = 'postgresql://postgres:27729212@localhost:5432/tesisdb'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
db.init_app(app)
migrate = Migrate(app, db)

# Habilitar CORS en todas las rutas
CORS(app)

# Registrar el blueprint de autenticación
app.register_blueprint(auth_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
