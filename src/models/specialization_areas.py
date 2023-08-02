from src.database.db import db

class SpecializationArea(db.Model):
    __tablename__ = 'specialization_areas'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    users = db.relationship('User', secondary='user_specializations', back_populates='specialization_areas')

    def __init__(self, name):
        self.name = name