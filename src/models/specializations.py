from src.database.db import db


class Specialization(db.Model):
    __tablename__ = 'specializations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    users = db.relationship(
        'User', secondary='user_specializations', back_populates='specializations')

    def __init__(self, name):
        self.name = name
