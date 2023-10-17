from flask import Blueprint, request, jsonify
from src.controllers.recommendation_controller import merge_courses
from src.models.skills import Skill
from src.models.specializations import Specialization
from src.models.users import User

recommendation_blueprint = Blueprint('recommendation', __name__)


@recommendation_blueprint.route('/recommendation', methods=['GET'])
def get_recommendation():
    token = request.headers.get('Authorization')

    current_user = User.query.filter_by(session_token=token).first()
    skills = Skill.query.all()
    specializations = Specialization.query.all()

    recommended_courses = merge_courses(current_user, skills, specializations)

    return jsonify({"data": recommended_courses})
