from flask import Blueprint, request, jsonify
from src.models.users import User
from src.database.db import db
from src.routes.linkedin_spider import run_linkedin_spider  # Importar la función desde linkedin_spider.py

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/signup', methods=['POST'])
def signup():
    data = request.json
    name = data.get('name')
    cedula = data.get('cedula')
    email = data.get('email')
    password = data.get('password')
    level_id = data.get('level_id')

    # Crear el nuevo usuario
    user = User(name=name, id_card=cedula, email=email, password=password, level_id=level_id)

    # Guardar el usuario en la base de datos
    db.session.add(user)
    try:
        db.session.commit()  # Confirmar la transacción

        # Llamar a la función del spider de LinkedIn después de registrar el usuario
        run_linkedin_spider()

        return jsonify({'message': 'Usuario registrado exitosamente'})
    except Exception as e:
        db.session.rollback()  # Deshacer la transacción en caso de error
        return jsonify({'error': 'Error al registrar el usuario', 'details': str(e)}), 500
