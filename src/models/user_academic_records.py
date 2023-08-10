from src.database.db import db


class UserAcademicRecord(db.Model):
    __tablename__ = 'user_academic_records'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    grade = db.Column(db.Numeric)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    # Relations
    user = db.relationship('User',
                           back_populates='user_academic_records')
