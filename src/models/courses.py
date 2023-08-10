from src.database.db import db


class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    # Assuming the actual date type is handled elsewhere.
    begin_date = db.Column(db.String)
    # Assuming the actual date type is handled elsewhere.
    end_date = db.Column(db.String)
    university = db.Column(db.String)
    requirements = db.Column(db.Text)
    level_id = db.Column(db.Integer, db.ForeignKey("levels.id"))
    url = db.Column(db.Text)
    career = db.Column(db.String)

    # Relations
    level = db.relationship('Level', back_populates='courses')
