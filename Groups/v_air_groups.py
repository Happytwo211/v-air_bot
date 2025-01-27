v_air_groups = {
    'id_1': 'Гимназия РУТ МИИТ',
    'id_2': 'Школа №1273'
}


def show_keys():
    result = []
    for keys in v_air_groups.keys():
        result.append(keys)
    return result


def show_values():
    result = []
    for value in v_air_groups.values():
        result.append(value)
        show_result = '\n'.join(result)

    return show_result

