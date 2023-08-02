from src.database.db import db

class UserPreference(db.Model):
    __tablename__ = 'user_preferences'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    rating = db.Column(db.Float)

    user = db.relationship('User', back_populates='preferences')
    course = db.relationship('Course', back_populates='users_preferences')

    def __init__(self, user_id, course_id, rating):
        self.user_id = user_id
        self.course_id = course_id
        self.rating = rating
