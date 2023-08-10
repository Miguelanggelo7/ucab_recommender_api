from src.database.db import db


class UserSkill(db.Model):
    __tablename__ = 'user_skills'

    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), primary_key=True)
    skill_id = db.Column(db.Integer, db.ForeignKey(
        'skills.id'), primary_key=True)

    def __init__(self, user_id, skill_id):
        self.user_id = user_id
        self.skill_id = skill_id
