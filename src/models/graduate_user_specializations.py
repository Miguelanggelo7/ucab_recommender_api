from src.database.db import db


class GraduateUserSpecialization(db.Model):
    __tablename__ = 'graduate_user_specializations'

    graduate_user_id = db.Column(db.Integer, db.ForeignKey(
        'graduate_users.id'), primary_key=True)
    specialization_id = db.Column(db.Integer, db.ForeignKey(
        'specializations.id'), primary_key=True)

    def __init__(self, user_id, specialization_id):
        self.user_id = user_id
        self.specialization_id = specialization_id
