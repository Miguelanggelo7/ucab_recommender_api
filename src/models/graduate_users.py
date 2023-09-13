from src.database.db import db


class GraduateUser(db.Model):
    __tablename__ = 'graduate_users'

    id = db.Column(db.Integer, primary_key=True)

    # Relations
    specializations = db.relationship(
        'Specialization', secondary='graduate_user_specializations', back_populates='graduate_users')
    skills = db.relationship(
        'Skill', secondary='graduate_user_skills', back_populates='graduate_users')
