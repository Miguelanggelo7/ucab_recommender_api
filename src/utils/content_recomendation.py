from unidecode import unidecode
import re


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
