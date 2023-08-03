from src.database.db import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    id_card = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    level_id = db.Column(db.Integer, db.ForeignKey('levels.id'), nullable=False)

    level = db.relationship('Level', back_populates='users')
    specializations = db.relationship('UserSpecialization', back_populates='users')

    def __init__(self, name, id_card, email, password, level_id):
        self.name = name
        self.id_card = id_card
        self.email = email
        self.password = password
        self.level_id = level_id
