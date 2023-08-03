from src.database.db import db

class Level(db.Model):
    __tablename__ = 'levels'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    users = db.relationship("User", back_populates="level")
    courses = db.relationship("Course", backref="level")