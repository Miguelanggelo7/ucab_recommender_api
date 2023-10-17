def binary_sum(*set):
    if not all(len(item) == len(set[0]) for item in set):
        raise ValueError("Todos los arrays deben tener la misma longitud")

    result = [0] * len(set[0])  # Inicializar el result con ceros

    for item in set:
        result = [result[i] or item[i] for i in range(len(result))]

    return result


def binary_sub(set, sub):
    if (len(set) != len(sub)):
        raise ValueError("Ambos conjuntos deben tener la misma longitud")

    result = []
    for i in range(0, len(set)):
        if sub[i] == 1:
            result.append(0)
        else:
            result.append(set[i])

    return result
