from src.database.db import db


class Skill(db.Model):
    __tablename__ = 'skills'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    # Relations
    users = db.relationship(
        'User', secondary='user_skills', back_populates='skills')
    graduate_users = db.relationship(
        'GraduateUser', secondary='graduate_user_skills', back_populates='skills')

    def __init__(self, name):
        self.name = name
