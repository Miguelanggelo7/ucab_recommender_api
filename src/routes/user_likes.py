from flask import Blueprint, request, jsonify
from src.database.db import db
from src.models.user_likes import UserLikes
from src.models.users import User
from src.models.skills import Skill
from src.models.specializations import Specialization


user_likes_blueprint = Blueprint('user_likes', __name__)


@user_likes_blueprint.route('/user_likes', methods=['POST'])
def create():
    token = request.headers.get('Authorization')
    user =  User.query.filter_by(session_token=token).first()
    
    data = request.json
    course_id = data.get("course_id")

    like = UserLikes.query.filter_by(user_id=user.id, course_id=course_id).first()
    if like is None:
        new_user_like = UserLikes(user.id, course_id)
        db.session.add(new_user_like)
    else:
        db.session.delete(like)

    db.session.commit()

    return jsonify({'message': 'Like guardado correctamente'}), 200

@user_likes_blueprint.route('/user_likes_show', methods=['GET'])
def show():
    token = request.headers.get('Authorization')
    user = User.query.filter_by(session_token=token).first()

    likes = UserLikes.query.filter_by(user_id=user.id).all()
    data = []

    for item in likes:
        course = Course.query.filter_by(id=item.course_id).first()
        data.append({
            "title": course.title,
            "career": course.career,
            "id": course.id,
            "description": course.description,
            "requirements": course.requirements,
            "url": course.url,
            "begin_date": course.begin_date,
            "end_date": course.end_date,
            "university": course.university,
            "level": course.level.name,
        })

    return jsonify({ "data": data }), 200