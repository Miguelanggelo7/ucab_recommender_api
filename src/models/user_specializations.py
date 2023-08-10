from src.database.db import db


class UserSpecialization(db.Model):
    __tablename__ = 'user_specializations'

    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), primary_key=True)
    specialization_id = db.Column(db.Integer, db.ForeignKey(
        'specializations.id'), primary_key=True)

    def __init__(self, user_id, specialization_id):
        self.user_id = user_id
        self.specialization_id = specialization_id
