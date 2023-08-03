from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from src.models.users import User
from src.database.db import db
from src.routes.linkedin_spider import run_linkedin_spider

auth_blueprint = Blueprint('auth', __name__)
bcrypt = Bcrypt()

@auth_blueprint.route('/signup', methods=['POST'])
def signup():
    data = request.json
    name = data.get('name')
    cedula = data.get('cedula')
    email = data.get('email')
    password = data.get('password')
    level_id = data.get('level_id')

    # Verificar si ya existe un usuario con la misma cédula o email
    existing_user_by_cedula = User.query.filter_by(id_card=cedula).first()
    existing_user_by_email = User.query.filter_by(email=email).first()

    if existing_user_by_cedula:
        return jsonify({'error': 'Ya existe un usuario con esta cédula'}), 400

    if existing_user_by_email:
        return jsonify({'error': 'Ya existe un usuario con este email'}), 400

    # Encriptar el password
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Crear el nuevo usuario
    user = User(name=name, id_card=cedula, email=email, password=hashed_password, level_id=level_id)

    # Guardar el usuario en la base de datos
    db.session.add(user)
    try:
        db.session.commit()
        run_linkedin_spider()
        return jsonify({'message': 'Usuario registrado exitosamente'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error al registrar el usuario', 'details': str(e)}), 500
