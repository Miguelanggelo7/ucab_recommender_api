from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_card = Column(String, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String)
    password = Column(String, nullable=False)
    level_id = Column(Integer, ForeignKey("level.id"))
    academic_records = relationship("UserAcademicRecord", backref="user")
