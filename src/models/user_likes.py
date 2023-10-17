from src.database.db import db


class UserLikes(db.Model):
    __tablename__ = 'user_likes'

    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey(
        'courses.id'), primary_key=True)

    def __init__(self, user_id, course_id):
        self.user_id = user_id
        self.course_id = course_id
