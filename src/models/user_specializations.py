from src.database.db import db

class UserSpecialization(db.Model):
    __tablename__ = 'user_specializations'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    specialization_area_id = db.Column(db.Integer, db.ForeignKey('specialization_areas.id'), primary_key=True)

    specialization_area = db.relationship('SpecializationArea', back_populates='users')
    user = db.relationship('User', back_populates='specialization_areas')
