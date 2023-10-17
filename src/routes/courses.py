from flask import Blueprint, jsonify
from src.models.courses import Course
from src.database.db import db

courses_blueprint = Blueprint('courses', __name__)

@courses_blueprint.route('/universities', methods=['GET'])
def get_unique_universities():
    # Consulta la base de datos para obtener las universidades de los cursos
    universities = db.session.query(Course.university).distinct().all()
    
    # Transforma el resultado en una lista de universidades únicas
    unique_universities = [university[0] for university in universities]
    
    return jsonify({'universities': unique_universities})

@courses_blueprint.route('/careers', methods=['GET'])
def get_unique_careers():
    # Consulta la base de datos para obtener las carreras de los cursos
    careers = db.session.query(Course.career).distinct().all()
    
    # Transforma el resultado en una lista de carreras únicas
    unique_careers = [career[0] for career in careers]
    
    return jsonify({'careers': unique_careers})