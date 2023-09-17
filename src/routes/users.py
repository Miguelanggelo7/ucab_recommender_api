from flask import Blueprint, request, jsonify
from src.models.users import User
from src.models.courses import Course
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.cluster import DBSCAN
from src.database.db import db
from src.models.graduate_users import GraduateUser
from src.models.skills import Skill
from src.models.specializations import Specialization
import numpy as np
# instalar
import spacy
from unidecode import unidecode
from gensim.models import Word2Vec
from sklearn.metrics.pairwise import cosine_similarity
import re
from src.utils.careers import careers
from src.utils.taxonomy import taxonomy

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


@users_blueprint.route('/content_recomendation', methods=['GET'])
def get_content_recomendation():
    token = request.headers.get('Authorization')
    courses = Course.query.all()

    user = User.query.filter_by(session_token=token).first()
    user_specializations = []
    user_skills = []

    for skill in user.skills:
        user_skills.append(skill.name)

    for specialization in user.specializations:
        user_specializations.append(specialization.name)

    courses_data = []
    for course in courses:
        data = {
            "title": course.title,
            "career": course.career,
            "id": "",
            # TODO: get description
            "description": course.requirements,
            "requirements": course.requirements
        }

        courses_data.append(data)

    # Cargar el modelo de spaCy
    nlp = spacy.load("es_core_news_md")

    # Crear documentos de texto para los vectores del usuario
    doc_user_skills = nlp(" ".join(user_skills))
    doc_user_expertise_areas = nlp(" ".join(user_specializations))
    doc_user_career = nlp(" ".join(careers))

    # Calcular el vector promedio del usuario
    user_vector = np.mean(
        [doc_user_skills.vector, doc_user_expertise_areas.vector, doc_user_career.vector], axis=0)

    # Calcular la similitud semántica y ordenar los cursos
    for course in courses_data:
        course_title = course["title"]
        course_career = course["career"]
        # course_description = course.get("description", "")
        course_requirements = course["requirements"]

        doc_course_title = nlp(course_title)
        doc_course_career = nlp(course_career)
        # doc_course_description = nlp(course_description)

        if course_requirements is not None:
            doc_course_requirements = nlp(course_requirements)

        else:
            print(f"Los requisitos del curso '{course_title}' son None. Se omite.")

        # Combinar título, carrera, descripción y requisitos en una cadena para el curso
        # combined_text = f"{course_title} {course_career} {course_description} {course_requirements}"
        combined_text = f"{course_title} {course_career} {course_requirements}"
        doc_combined_text = nlp(combined_text)

        # Calcular el vector para el texto combinado
        course_vector = doc_combined_text.vector

        # Calcular la similitud semántica entre el usuario y el curso
        similarity_text = np.dot(user_vector, course_vector) / \
            (np.linalg.norm(user_vector) * np.linalg.norm(course_vector))

        # Calcular la distancia jerárquica mínima para cada habilidad del usuario
        similarities_taxonomy = [hierarchical_distance(
            taxonomy, interest, combined_text) for interest in user_skills + user_specializations]

        # Verificar si la carrera del curso está en las carreras del usuario
        if unidecode(course_career.lower()) in careers:
            # Tomar el valor mínimo de las similitudes jerárquicas
            similarity_taxonomy = min(similarities_taxonomy)
        else:
            # Asignar 1 si la carrera del curso no coincide con la del usuario
            similarity_taxonomy = 1

        # Calcular la similitud total ponderada
        total_similarity = 0.6 * similarity_text + \
            0.4 * (1 - similarity_taxonomy)
        # total_similarity = (1 - similarity_taxonomy)

        course["total_similarity"] = total_similarity

    # Ordenar los cursos por similitud en orden descendente
    sorted_courses = sorted(
        courses_data, key=lambda x: x["total_similarity"], reverse=True)

    # Imprimir los cursos ordenados por similitud
    for course in sorted_courses:
        print(
            f"Título: {course['title']}, Similaridad Total: {course['total_similarity']:.4f}")

    return jsonify({'data': sorted_courses})


def remove_special_chars(text):
    # Remover caracteres especiales y convertir a minúsculas
    text = unidecode(text).lower()
    # Eliminar espacios en blanco adicionales
    text = ' '.join(text.split())
    return text


def find_taxonomy_substring(input_string, taxonomy):
    input_string = remove_special_chars(input_string)
    for category, subcategories in taxonomy.items():
        category_cleaned = remove_special_chars(category)
        if category_cleaned in input_string:
            return category
        if isinstance(subcategories, dict):
            result = find_taxonomy_substring(input_string, subcategories)
            if result:
                return result
        elif isinstance(subcategories, set):
            for sub_subcategory in subcategories:
                sub_subcategory_cleaned = remove_special_chars(sub_subcategory)
                if sub_subcategory_cleaned in input_string:
                    return sub_subcategory
                elif "(" in sub_subcategory and ")" in sub_subcategory:
                    # Si sub_subcategory contiene paréntesis, verificar si su versión abreviada entre paréntesis coincide
                    sub_subcategory_abbr = re.search(
                        r'\((.*?)\)', sub_subcategory).group(1)
                    if sub_subcategory_abbr and sub_subcategory_abbr in input_string:
                        return sub_subcategory
    return None


def title_contains_taxonomy_substring(input_string, taxonomy):
    input_string = remove_special_chars(input_string)
    result = find_taxonomy_substring(input_string, taxonomy)
    return result is not None


def find_depth_and_parent(node, target, parent=None, depth=0):
    if isinstance(node, dict):
        if target in node:
            return depth, parent
        for key, value in node.items():
            result = find_depth_and_parent(
                value, target, parent=key, depth=depth + 1)
            if result[0] is not None:
                return result

    return None, None


def find_taxonomy_parent(word, taxonomy):
    # Manejar el caso especial en el que word es igual a "ingenieria en informatica"
    if word == "ingenieria en informatica":
        return word

    for parent, children in taxonomy.items():
        if word in children:
            return parent
        else:
            # Si el padre tiene hijos, busca recursivamente en ellos
            if isinstance(children, dict):
                result = find_taxonomy_parent(word, children)
                if result:
                    return result


def calculate_distance(taxonomy, str1, str2):
    parent1 = find_taxonomy_parent(str1, taxonomy)
    parent2 = find_taxonomy_parent(str2, taxonomy)

    if parent1 == parent2:
        return 0.2  # Los conceptos están en el mismo nivel de la jerarquía

    # Calcular la distancia ascendiendo en la jerarquía
    distance = 0.2
    while parent1 != parent2:
        # Añadir 0.2 por cada nivel ascendido
        distance += 0.2
        # Moverse un nivel hacia arriba en la jerarquía
        parent1 = find_taxonomy_parent(parent1, taxonomy)
        parent2 = find_taxonomy_parent(parent2, taxonomy)

    return 1 if distance > 1 else distance


def hierarchical_distance(taxonomy, concept1, concept2):
    # Convertir a minúsculas y quitar acentos
    concept1_lower = unidecode(concept1.lower())
    # Convertir a minúsculas y quitar acentos
    concept2_lower = unidecode(concept2.lower())

    if concept1_lower == concept2_lower:
        return 0.0

    # Verifica si el concepto 1 está contenido en el concepto 2 o viceversa (insensible a mayúsculas/minúsculas).
    if concept1_lower in concept2_lower or concept2_lower in concept1_lower:
        return 0.0

    if title_contains_taxonomy_substring(concept2_lower, taxonomy) and title_contains_taxonomy_substring(concept1_lower, taxonomy):

        result1 = find_taxonomy_substring(concept1_lower, taxonomy)
        result2 = find_taxonomy_substring(concept2_lower, taxonomy)

        distance = calculate_distance(taxonomy, result1, result2)

        if distance is not None:
            return distance
        else:
            print(
                f"No se encontraron '{result1}' y '{result2}' en la jerarquía.")

    return 0.6
