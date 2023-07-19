from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Text

Base = declarative_base()


class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    # dates are strings and in db are date
    begin_date = Column(String)
    end_date = Column(String)
    university = Column(String)
    requirements = Column(Text)
    level_id = Column(Integer, ForeignKey("level.id"))
    country_id = Column(Integer, ForeignKey("country.id"))
