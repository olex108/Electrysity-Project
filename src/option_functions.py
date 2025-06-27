import os
import copy
import parameters
from src.data_functions import add_to_json_file, get_data, replace_in_json_file
import calculate_estimate


def create_new_project():
    """
    Функция запрашивает у пользователя параметры по шаблону "project_name_parameters" словарю.
    Создает словарь с данными пользователя после чего вызывает функцию для записи данных
    в базу "list_of_projects_name.json"
    Вызывает функцию открытия данных проекта open_project()

    * требует доработки для проверки данных на совпадения имен и паролей
    """

    new_project_name = {}
    # Запрашиваем по очереди параметры из словаря заготовки
    for key, value in parameters.project_name_parameters.items():
        new_project_name[key] = input(f"{key} {value}:")
    # вызов функции для добавления данных в JSON
    add_to_json_file(
        os.path.abspath(os.path.join(os.pardir, "data", "list_of_projects_name.json")),
        new_project_name,
    )
    open_project(new_project_name)


def verification_name_password():
    """
    Функция запрашивает имя проекта, проверяет пароль.
    Вызывает функцию open_project, для работы с проектом
    """

    user_project_name = input("Введите название проекта")
    list_of_projects_name = get_data(os.path.join(os.pardir, "data", "list_of_projects_name.json"))

    not_in_project_names = True

    for project_name_data in list_of_projects_name:
        if project_name_data["Название"] == user_project_name:
            not_in_project_names = False
            while True:
                project_password = input("Введите пароль")
                if project_password == project_name_data["Пароль"]:
                    open_project(project_name_data)
                    break
                else:
                    print("Пароль не верный!")

    if not_in_project_names:
        print(f"{user_project_name} не найден!")
        verification_name_password()


def open_project(project_name_data: dict):
    """
    Функция принимает словарь с именными данными проекта.
    Проверяет внесены ли по этому названию данные.

    Если да позволяет посмотреть, изменить или расчитать стоимость работ
    Если нет вызывает функцию для записи параметров
    :param project_name_data:
    :return:
    """

    # Выводим словарь в виде таблицы
    print_dictionary_lines(project_name_data)

    list_of_projects_parameters = get_data(os.path.join(os.pardir, "data", "list_of_projects_parameters.json"))

    not_in_project_name_data = True

    for project_parameters in list_of_projects_parameters:
        if project_name_data["Название"] == project_parameters["Название"]:
            not_in_project_name_data = False
            print("Данные проекта внесены")
            option = input(f"Выберите действие:\nПосмотреть данные\nИзменить данные\nРасчитать стоимость работ\n")

            if option == "Посмотреть данные":
                print_dictionary_lines(project_parameters)
                open_project(project_name_data)

            elif option == "Изменить данные":
                change_project_parameters(project_name_data, project_parameters)
                open_project(project_name_data)

            elif option == "Расчитать стоимость работ":
                estimate_dictionary = calculate_estimate.calculate_estimate(project_parameters)
                print_dictionary_lines(estimate_dictionary)
                open_project(project_name_data)

    if not_in_project_name_data:
        option = input(f"Выберите действие:\nВнести данные?Да/Нет\n")
        if option == "Да":
            create_project_parameters(project_name_data, parameters.project_parameters)


def print_dictionary_lines(dictionary_data: dict):
    """
    Функция для построчного вывода данных из формы словаря в строчный вид с задекорированными тире
    """

    print("-" * 10)
    print(*[f"{key}: {value}" for key, value in dictionary_data.items()], sep="\n")
    print("-" * 10)


def create_project_parameters(project_name_data: dict, dictionary_data: dict):
    """Функция для записи параметров проекта
    Принимает словарь названия проекта и словарь для внесения или изменения параметров
    Записывает данные в list_of_projects_parameters.json"""

    new_project_parameters = copy.deepcopy(dictionary_data)

    for key, value in new_project_parameters.items():

        if key == "Название":
            new_project_parameters["Название"] = project_name_data["Название"]
            print(f"{key}: {new_project_parameters["Название"]}")

        elif key == "Тип проекта":
            new_project_parameters["Тип проекта"] = project_name_data["Тип проекта"]
            print(f"{key}: {new_project_parameters["Тип проекта"]}")

        elif key == "Площадь помещения":
            new_project_parameters["Площадь помещения"] = project_name_data["Площадь помещения"]
            print(f"{key}: {new_project_parameters["Площадь помещения"]}")

        else:
            print(f"{key}: {new_project_parameters[key]}")
            new_project_parameters[key] = input("Внести:")

    add_to_json_file(
        os.path.abspath(os.path.join(os.pardir, "data", "list_of_projects_parameters.json")),
        new_project_parameters,
    )

    print_dictionary_lines(new_project_parameters)

    open_project(project_name_data)


def change_project_parameters(project_name_data: dict, dictionary_data: dict):
    """Функция для записи параметров проекта
    Принимает словарь названия проекта и словарь для внесения или изменения параметров
    Записывает данные в list_of_projects_parameters.json"""

    new_project_parameters = copy.deepcopy(dictionary_data)

    for key, value in new_project_parameters.items():

        if key == "Название":
            new_project_parameters["Название"] = project_name_data["Название"]
            print(f"{key}: {new_project_parameters["Название"]}")

        elif key == "Тип проекта":
            new_project_parameters["Тип проекта"] = project_name_data["Тип проекта"]
            print(f"{key}: {new_project_parameters["Тип проекта"]}")

        elif key == "Площадь помещения":
            new_project_parameters["Площадь помещения"] = project_name_data["Площадь помещения"]
            print(f"{key}: {new_project_parameters["Площадь помещения"]}")

        else:
            print(f"{key}: {new_project_parameters[key]}")
            new_project_parameters[key] = input("Внести:")

    replace_in_json_file(
        os.path.abspath(os.path.join(os.pardir, "data", "list_of_projects_parameters.json")),
        new_project_parameters,
    )

    print_dictionary_lines(new_project_parameters)

    open_project(project_name_data)


