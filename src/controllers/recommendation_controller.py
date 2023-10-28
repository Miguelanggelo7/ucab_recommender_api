from sqlalchemy import func
from src.models.graduate_users import GraduateUser
from src.models.skills import Skill
from src.models.specializations import Specialization
from src.models.user_likes import UserLikes
from src.models.users import User
from src.models.courses import Course
import numpy as np
import spacy
from unidecode import unidecode
from src.utils.careers import careers
from src.utils.taxonomy import taxonomy
from src.utils.content_recomendation import hierarchical_distance
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

from src.utils.collaborative_filtering import binary_sub, binary_sum

N_CLUSTERS = 5


def content_filtering_process(user_skills, user_specializations):
    courses = Course.query.all()
    nlp = spacy.load("es_core_news_md")

    courses_data = []
    for course in courses:
        data = {
            "title": course.title,
            "career": course.career,
            "id": course.id,
            "description": course.description,
            "requirements": course.requirements,
        }

        courses_data.append(data)

    doc_user_skills = nlp(" ".join(user_skills))
    doc_user_expertise_areas = nlp(" ".join(user_specializations))
    doc_user_career = nlp(" ".join(careers))

    user_vector = np.mean(
        [doc_user_skills.vector, doc_user_expertise_areas.vector, doc_user_career.vector], axis=0)

    for course in courses_data:
        course_title = course["title"]
        course_career = course["career"]
        course_description = course["description"]
        course_requirements = course["requirements"]

        # Combinar título, carrera, descripción y requisitos en una cadena para el curso
        combined_text = f"{course_title} {course_career} {course_description} {course_requirements}"
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
            if similarities_taxonomy:
                similarity_taxonomy = min(similarities_taxonomy)
            else:
                similarity_taxonomy = 0
        else:
            # Asignar 1 si la carrera del curso no coincide con la del usuario
            similarity_taxonomy = 1

        # Calcular la similitud total ponderada
        total_similarity = 0.6 * similarity_text + \
            0.4 * (1 - similarity_taxonomy)
        # total_similarity = (1 - similarity_taxonomy)

        course["similarity"] = total_similarity

    sorted_courses = sorted(
        courses_data, key=lambda x: x["similarity"], reverse=True)
    return sorted_courses


def colaborative_filtering_process(data):
    combined_matrix = np.array(data)
    kmeans = KMeans(n_clusters=N_CLUSTERS)
    kmeans.fit(combined_matrix)

    cluster_tags = kmeans.labels_

    return cluster_tags


def collaborative_based_in_graduate_users(current_user, skills, specializations):
    graduate_users = GraduateUser.query.all()
    users_data = []

    for user in [current_user, *graduate_users]:
        users_data.append({
            'id': user.id,
            'skills': [0] * (Skill.query.count()),
            'specializations': [0] * (Specialization.query.count()),
        })

        i = 0
        for skill in skills:
            if skill in user.skills:
                users_data[-1]["skills"][i] = 1
            i += 1

        i = 0
        for specialization in specializations:
            if specialization in user.specializations:
                users_data[-1]["specializations"][i] = 1
            i += 1

    cluster_tags = colaborative_filtering_process(
        [user['skills'] + user['specializations'] for user in users_data])

    i = 0
    for user in users_data:
        user["cluster"] = cluster_tags[i]
        i += 1

    cluster_data = [
        user for user in users_data if user["cluster"] == cluster_tags[0]]
    # Se resta el vector resultante menos el vector del usuario
    skills_result = binary_sub(binary_sum(
        *list(map(lambda item: item["skills"], cluster_data))), cluster_data[0]["skills"])
    specializations_result = binary_sub(binary_sum(
        *list(map(lambda item: item["specializations"], cluster_data))), cluster_data[0]["specializations"])

    skills_data = []
    specializations_data = []

    i = 0
    for skill in skills:
        if skills_result[i] == 1:
            skills_data.append(skill.name)
        i += 1

    i = 0
    for specialization in specializations:
        if specializations_result[i] == 1:
            specializations_data.append(specialization.name)
        i += 1

    sorted_courses = content_filtering_process(
        skills_data, specializations_data)
    return sorted_courses


def collavorative_based_in_liked_courses(current_user, skills, specializations):
    users = User.query.all()
    users_data = []

    for user in users:
        users_data.append({
            'id': user.id,
            'skills': [0] * (Skill.query.count()),
            'specializations': [0] * (Specialization.query.count()),
        })

        i = 0
        for skill in skills:
            if skill in user.skills:
                users_data[-1]["skills"][i] = 1
            i += 1

        i = 0
        for specialization in specializations:
            if specialization in user.specializations:
                users_data[-1]["specializations"][i] = 1
            i += 1

    cluster_tags = colaborative_filtering_process(
        [user['skills'] + user['specializations'] for user in users_data])

    i = 0

    current_user_cluster = 0
    for user in users_data:
        user["cluster"] = cluster_tags[i]
        if user["id"] == current_user.id:
            current_user_cluster = cluster_tags[i]
        i += 1

    cluster_ids = [
        user["id"] for user in users_data if user["cluster"] == current_user_cluster]

    # Se obtienen los ids de las materias con mas likes primero
    likes = UserLikes.query.with_entities(UserLikes.course_id, func.count(UserLikes.course_id).label("count"))\
        .filter(UserLikes.user_id.in_(cluster_ids))\
        .group_by(UserLikes.course_id)\
        .order_by(func.count(UserLikes.course_id).desc()).all()

    min_count = min(like.count for like in likes)
    max_count = max(like.count for like in likes)

    courses_data = []
    for item in likes:
        course = Course.query.get(item.course_id)
        data = {
            "title": course.title,
            "career": course.career,
            "id": course.id,
            "description": course.description,
            "requirements": course.requirements,
            "count": item.count
        }
        courses_data.append(data)

    repetitions_counts = [course['count']
                          for course in courses_data]
    if all(count == repetitions_counts[0] for count in repetitions_counts):
        for course in courses_data:
            course['similarity'] = 1
    else:
        # Calcular el intervalo de similitud
        interval = (1 - 0.7) / (max_count -
                                min_count) if max_count != min_count else 0

        # Asignar similitud a cada curso
        for course in courses_data:
            repetitions_count = course['count']
            course['similarity'] = 0.7 + \
                (repetitions_count - min_count) * interval

    # Ordenar los cursos por similitud de mayor a menor
    courses_data = sorted(
        courses_data, key=lambda x: x['similarity'], reverse=True)

    for item in courses_data:
        del item["count"]

    return courses_data


def content_filtering(current_user):
    user_specializations = []
    user_skills = []

    for skill in current_user.skills:
        user_skills.append(skill.name)

    for specialization in current_user.specializations:
        user_specializations.append(specialization.name)

    sorted_courses = content_filtering_process(
        user_skills, user_specializations)

    return sorted_courses


def merge_content_filtering_with_graduate_users(current_user, skills, specializations):
    content_recommendation = content_filtering(current_user)
    graduate_users_recommendation = collaborative_based_in_graduate_users(
        current_user, skills, specializations)

    courses = Course.query.all()
    courses_data = []
    for course in courses:
        content_item = next(
            (item for item in content_recommendation if item["id"] == course.id), None)
        graduate_users_item = next(
            (item for item in graduate_users_recommendation if item["id"] == course.id), None)

        data = dict(content_item)
        data["similarity"] = (content_item["similarity"] +
                              graduate_users_item["similarity"]) / 2
        courses_data.append(data)

    courses_data = sorted(
        courses_data, key=lambda x: x['similarity'], reverse=True)

    return courses_data


def elbow_method_graduate_users(skills, specializations):
    graduate_users = GraduateUser.query.all()
    users_data = []
    skills_len = len(skills)
    specializations_len = len(specializations)

    for user in graduate_users:
        users_data.append({
            'id': user.id,
            'skills': [0] * skills_len,
            'specializations': [0] * specializations_len,
        })

        i = 0
        for skill in skills:
            if skill in user.skills:
                users_data[-1]["skills"][i] = 1
            i += 1

        i = 0
        for specialization in specializations:
            if specialization in user.specializations:
                users_data[-1]["specializations"][i] = 1
            i += 1

    data = [user['skills'] + user['specializations'] for user in users_data]
    inertia = []
    combined_matrix = np.array(data)
    max_lenght = len(users_data) + 1

    for i in range(1, max_lenght):
        kmeans = KMeans(n_clusters=i, random_state=0)
        kmeans.fit(combined_matrix)
        inertia.append(kmeans.inertia_)

    plt.figure(figsize=(10, 6))
    plt.plot(range(1, max_lenght), inertia, marker='o')
    plt.title('Método del Codo')
    plt.xlabel('Número de Clústeres')
    plt.ylabel('Inercia')
    plt.savefig("metodo_del_codo_egresados.png")


def elbow_method_users(skills, specializations):
    users = User.query.all()
    users_data = []
    skills_len = len(skills)
    specializations_len = len(specializations)

    for user in users:
        users_data.append({
            'id': user.id,
            'skills': [0] * skills_len,
            'specializations': [0] * specializations_len,
        })

        i = 0
        for skill in skills:
            if skill in user.skills:
                users_data[-1]["skills"][i] = 1
            i += 1

        i = 0
        for specialization in specializations:
            if specialization in user.specializations:
                users_data[-1]["specializations"][i] = 1
            i += 1

    data = [user['skills'] + user['specializations'] for user in users_data]
    inertia = []
    combined_matrix = np.array(data)
    max_lenght = len(users_data) + 1

    for i in range(1, max_lenght):
        kmeans = KMeans(n_clusters=i, random_state=0)
        kmeans.fit(combined_matrix)
        inertia.append(kmeans.inertia_)

    plt.figure(figsize=(10, 6))
    plt.plot(range(1, max_lenght), inertia, marker='o')
    plt.title('Método del Codo')
    plt.xlabel('Número de Clústeres')
    plt.ylabel('Inercia')
    plt.savefig("metodo_del_codo_usuarios.png")


def merge_courses(current_user, skills, specializations):
    merged_courses = {}
    content_and_graduate_users_recommendation = merge_content_filtering_with_graduate_users(
        current_user, skills, specializations)
    courses_liked_recommendation = collavorative_based_in_liked_courses(
        current_user, skills, specializations)

    # Agregar cursos del primer array al diccionario
    for course in content_and_graduate_users_recommendation:
        id = course['id']
        if id not in merged_courses or course['similarity'] > merged_courses[id]['similarity']:
            merged_courses[id] = course

    # Agregar cursos del segundo array al diccionario
    for course in courses_liked_recommendation:
        id = course['id']
        if id not in merged_courses or course['similarity'] > merged_courses[id]['similarity']:
            merged_courses[id] = course

    # Convertir el diccionario nuevamente en una lista
    merged_courses_list = list(merged_courses.values())

    # Ordenar la lista por similitud de mayor a menor
    merged_courses_list = sorted(
        merged_courses_list, key=lambda x: x['similarity'], reverse=True)
    return merged_courses_list
