from src.database.db import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_card = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String)
    password = db.Column(db.String, nullable=False)
    level_id = db.Column(db.Integer, db.ForeignKey("levels.id"))
    academic_records = db.relationship("UserAcademicRecord", backref="user")