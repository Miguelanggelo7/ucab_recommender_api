from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt, check_password_hash
from src.models.users import User
from src.models.skills import Skill
from src.models.specializations import Specialization
from src.database.db import db
from flask_jwt_extended import create_access_token, JWTManager, jwt_required, get_jwt_identity

auth_blueprint = Blueprint('auth', __name__)
bcrypt = Bcrypt()


@auth_blueprint.route('/signup', methods=['POST'])
def signup():
    data = request.json
    name = data.get('name')
    id_card = data.get('id_card')
    email = data.get('email')
    password = data.get('password')
    level_id = data.get('level_id')
    skills_array = data.get('skills') or []
    specializations_array = data.get('specializations') or []

    # Verificar si ya existe un usuario con la misma cédula o email
    existing_user_by_id_card = User.query.filter_by(id_card=id_card).first()
    existing_user_by_email = User.query.filter_by(email=email).first()

    if existing_user_by_id_card:
        return jsonify({'error': 'Ya existe un usuario con esta cédula'}), 400

    if existing_user_by_email:
        return jsonify({'error': 'Ya existe un usuario con este email'}), 400

    # Encriptar el password
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Crear el nuevo usuario
    access_token = create_access_token(identity=id_card)
    user = User(name=name, id_card=id_card, email=email,
                password=hashed_password, level_id=level_id, session_token=access_token)

    # Guardar el usuario en la base de datos
    db.session.add(user)

    for skill_name in skills_array:
        skill_name = skill_name.strip().lower()
        skill = Skill.query.filter_by(name=skill_name).first()

        if not skill:
            skill = Skill(name=skill_name)
            db.session.add(skill)

        user.skills.append(skill)

    for specialization_name in specializations_array:
        specialization_name = specialization_name.strip().lower()
        specialization = Specialization.query.filter_by(
            name=specialization_name).first()

        if not specialization:
            specialization = Specialization(name=specialization_name)
            db.session.add(specialization)

        user.specializations.append(specialization)

    try:
        db.session.commit()

        user_json = {
            "name": user.name,
            "id_card": user.id_card,
            "email": user.email,
            "level": user.level.name
        }

        return jsonify({'message': 'Usuario registrado exitosamente', 'user': user_json, 'access_token': access_token}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error al registrar el usuario', 'details': str(e)}), 500


@auth_blueprint.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = User.query.filter_by(email=email).first()

    if user is None or not check_password_hash(user.password, password):
        return jsonify({'message': 'Credenciales de inicio de sesion incorrectas'}), 401

    try:
        access_token = create_access_token(identity=user.id_card)
        user.session_token = access_token
        db.session.commit()

        user_json = {
            "name": user.name,
            "id_card": user.id_card,
            "email": user.email,
            "level": user.level.name
        }

        return jsonify({'message': 'Usuario logueado exitosamente', 'user': user_json, 'access_token': access_token}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error al registrar el usuario', 'details': str(e)}), 500


@auth_blueprint.route('/logout', methods=['GET'])
def logout():
    token = request.headers.get('Authorization')

    user = User.query.filter_by(session_token=token).first()

    if user:
        user.session_token = None
        db.session.commit()
        return jsonify({"message": "Logout exitoso"})
    return jsonify({"error": "Token inválido"}), 401

@auth_blueprint.route('/get_user', methods=['GET'])
def get_user():
    token = request.headers.get('Authorization')
    user =  User.query.filter_by(session_token=token).first()

    if user:
        # Si se encuentra el usuario, devolvemos sus datos en formato JSON
        specializations = [item.name for item in user.specializations]
        skills = [item.name for item in user.skills]

        user_json = {
            "name": user.name,
            "id_card": user.id_card,
            "email": user.email,
            "level_id": user.level_id,
            "specializations": specializations,
            "skills": skills
        }
        return jsonify({"user": user_json}), 200
    else:
        # Si el usuario no se encuentra, devolvemos un error 404 (no encontrado)
        return jsonify({"error": "Usuario no encontrado"}), 404