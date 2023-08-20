from src.database.db import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    id_card = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    session_token = db.Column(db.Text, default=None)
    level_id = db.Column(db.Integer, db.ForeignKey('levels.id'))

    # Relations
    level = db.relationship('Level', back_populates='users')
    academic_records = db.relationship(
        'UserAcademicRecord', back_populates='user')
    specializations = db.relationship(
        'Specialization', secondary='user_specializations', back_populates='users')
    skills = db.relationship(
        'Skill', secondary='user_skills', back_populates='users')

    def __init__(self, name, id_card, email, password, level_id, session_token):
        self.name = name
        self.id_card = id_card
        self.email = email
        self.password = password
        self.level_id = level_id
        self.session_token = session_token
