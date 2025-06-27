import json


def get_data(json_file):
    """
    Функция для получения данных из файла JSON
    :param json_file:
    :return: data
    """

    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data


def add_to_json_file(json_file, add_data):
    """
    Функция для добавления данных в файл JSON

    :param json_file: адрес JSON файла
    :param add_data: данные для добавления в файл
    :return:
    """

    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    data.append(add_data)

    with open(json_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def replace_in_json_file(json_file, add_data):
    """
    Функция для добавления данных в файл JSON

    :param json_file: адрес JSON файла
    :param add_data: данные для добавления в файл
    :return:
    """

    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    for index, value in enumerate(data):
        if value["Название"] == add_data["Название"]:
            del data[index]

    data.append(add_data)

    with open(json_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
