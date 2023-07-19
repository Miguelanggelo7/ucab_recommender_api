from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class Level(Base):
    __tablename__ = 'levels'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    users = relationship("User", backref="level")
    courses = relationship("Course", backref="level")
