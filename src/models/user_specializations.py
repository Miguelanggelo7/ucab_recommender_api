from src.database.db import db

class UserSpecialization(db.Model):
    __tablename__ = 'user_specializations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    specialization_area_id = db.Column(db.Integer, db.ForeignKey('specialization_areas.id'), nullable=False)

    specialization_area = db.relationship('SpecializationArea', back_populates='user_specializations')
    user = db.relationship('User', back_populates='specializations')

    def __init__(self, user_id, specialization_area_id):
        self.user_id = user_id
        self.specialization_area_id = specialization_area_id
