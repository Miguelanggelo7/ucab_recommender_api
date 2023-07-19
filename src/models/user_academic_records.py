from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey

Base = declarative_base()


class UserAcademicRecord(Base):
    __tablename__ = 'user_academic_records'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    grade = Column(Numeric)
    user_id = Column(Integer, ForeignKey("user.id"))
