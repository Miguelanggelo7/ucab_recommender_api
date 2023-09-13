from src.database.db import db


class GraduateUserSkill(db.Model):
    __tablename__ = 'graduate_user_skills'

    graduate_user_id = db.Column(db.Integer, db.ForeignKey(
        'graduate_users.id'), primary_key=True)
    skill_id = db.Column(db.Integer, db.ForeignKey(
        'skills.id'), primary_key=True)

    def __init__(self, user_id, skill_id):
        self.graduate_user_id = user_id
        self.skills_id = skill_id
