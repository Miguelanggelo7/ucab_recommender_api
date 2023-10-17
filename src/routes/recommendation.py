from flask import Blueprint, request, jsonify
from controllers.recommendation_controller import content_filtering, collaborative_based_in_graduate_users, collavorative_based_in_liked_courses

from models.courses import Course
from models.skills import Skill
from models.specializations import Specialization
from models.users import User

recommendation_blueprint = Blueprint('recommendation', __name__)


@recommendation_blueprint.route('/recommendation', methods=['GET'])
def get_recommendation():
    token = request.headers.get('Authorization')

    current_user = User.query.filter_by(session_token=token).first()
    courses = Course.query.all()
    skills = Skill.query.all()
    specializations = Specialization.query.all()

    content_recommendation = content_filtering(current_user)
    graduate_users_recommendation = collaborative_based_in_graduate_users(
        current_user, skills, specializations)
    courses_liked_recommendation = collavorative_based_in_liked_courses(
        current_user, skills, specializations)

    # AQUI HACER LOS DEMAS PROCESOS

    return
