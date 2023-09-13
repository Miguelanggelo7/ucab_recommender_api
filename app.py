from flask import Flask
from src.routes.auth import auth_blueprint
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from decouple import config
from src.routes.auth import auth_blueprint
from src.routes.users import users_blueprint
from src.database.db import db
from decouple import config

from src.models.user_academic_records import UserAcademicRecord
from src.models.specializations import Specialization
from src.models.skills import Skill
from src.models.user_specializations import UserSpecialization
from src.models.user_skills import UserSkill
from src.models.users import User
from src.models.levels import Level
from src.models.courses import Course


app = Flask(__name__)


# configure_logging()
# scheduler = TwistedScheduler()
# scheduler.add_job(run_spiders, 'interval', seconds=30)
# scheduler.start()
# reactor.run()


# with app.app_context():
#     statement = select(Level).filter_by(name="pregrado")
#     session = get_session()
#     print(session.scalars(statement).first().id)


# Habilitar CORS en todas las rutas
CORS(app)


app.config["JWT_SECRET_KEY"] = config("JWT_SECRET_KEY")
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600 * 24 * 14
jwt = JWTManager(app)

# Init DB
user = config("DB_USER")
password = config("DB_PASS")
host = config("DB_HOST")
port = config("DB_PORT")
db_name = config("DB_NAME")
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
db.init_app(app)

# Routes
app.register_blueprint(auth_blueprint)
app.register_blueprint(users_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
