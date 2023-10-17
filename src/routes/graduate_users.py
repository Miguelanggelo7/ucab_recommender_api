from flask import Blueprint, request, jsonify
from src.database.db import db
from src.models.graduate_users import GraduateUser
from src.models.skills import Skill
from src.models.specializations import Specialization


graduate_users_blueprint = Blueprint('graduate_users', __name__)


@graduate_users_blueprint.route('/graduate_users', methods=['POST'])
def create_graduate_user():
    data = request.json
    skills_array = data.get('skills') or []
    specializations_array = data.get('specializations') or []

    graduate_user = GraduateUser()
    db.session.add(graduate_user)

    for skill_name in skills_array:
        skill_name = skill_name.strip().lower()
        skill = Skill.query.filter_by(name=skill_name).first()

        if not skill:
            skill = Skill(name=skill_name)
            db.session.add(skill)

        graduate_user.skills.append(skill)

    for specialization_name in specializations_array:
        specialization_name = specialization_name.strip().lower()
        specialization = Specialization.query.filter_by(
            name=specialization_name).first()

        if not specialization:
            specialization = Specialization(name=specialization_name)
            db.session.add(specialization)

        graduate_user.specializations.append(specialization)

    db.session.commit()

    return jsonify({'message': 'Usuario registrado exitosamente'}), 200
