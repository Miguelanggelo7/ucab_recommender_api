from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy

# Crea una instancia de SQLAlchemy
db = SQLAlchemy()

def get_engine(user, password, host, port, db):
    url = f"postgresql://{user}:{password}@{host}:{port}/{db}"
    engine = create_engine(url)
    return engine


def get_engine_from_settings():
    return get_engine(
        config("DB_USER"),
        config("DB_PASS"),
        config("DB_HOST"),
        config("DB_PORT"),
        config("DB_NAME"),
    )


def get_session():
    engine = get_engine_from_settings()
    return sessionmaker(bind=engine)()
