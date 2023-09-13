from flask import Blueprint, request, jsonify
from src.models.users import User
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.cluster import DBSCAN
from src.database.db import db
from src.models.graduate_users import GraduateUser
from src.models.skills import Skill
from src.models.specializations import Specialization
import numpy as np

users_blueprint = Blueprint('users', __name__)


@users_blueprint.route('/graduate_users', methods=['POST'])
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


@users_blueprint.route('/clusters', methods=['GET'])
def get_clusters_by_users():
    users = User.query.all()
    users_data = []
    users_skills = []
    users_specializations = []

    for user in users:
        users_data.append({
            'name': user.name,
            'skills': [],
            'specializations': [],
            'level': user.level.name
        })

        for skill in user.skills:
            users_data[-1]["skills"].append(skill.name)
        if users_data[-1]["skills"]:
            users_skills.append(users_data[-1]["skills"])

        for specialization in user.specializations:
            users_data[-1]["specializations"].append(specialization.name)
        if users_data[-1]["specializations"]:
            users_specializations.append(users_data[-1]["specializations"])

    mlb = MultiLabelBinarizer()
    x_skills = mlb.fit_transform(users_skills)
    x_specializations = mlb.fit_transform(users_specializations)

    matrix = np.hstack((x_skills, x_specializations))

    dbscan = DBSCAN(eps=0.5, min_samples=5)
    clusters = dbscan.fit_predict(matrix)

    return jsonify({'users': users_data})
