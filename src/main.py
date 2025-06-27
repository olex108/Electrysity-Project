import option_functions

from src.data_functions import add_to_json_file, get_data

import parameters

import os

import calculate_estimate


def select_option():
    """
    Функция выбора действия пользователя запускается при вызове программы и предлагает
    пользователю варианты действий:
    - Создать новый проект
    - Открыть существующий проект
    """

    operation = input(f"Выберите действие:\nСоздать новый проект\nОткрыть существующий проект\nРасценки\n")

    if operation == "Создать новый проект":
        option_functions.create_new_project()
    elif operation == "Открыть существующий проект":
        option_functions.verification_name_password()
    elif operation == "Расценки":
        option_functions.print_dictionary_lines(parameters.price_list)

    select_option()


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
    option_functions.print_dictionary_lines(project_name_data)

    list_of_projects_parameters = get_data(os.path.join(os.pardir, "data", "list_of_projects_parameters.json"))

    not_in_project_name_data = True

    for project_parameters in list_of_projects_parameters:
        if project_name_data["Название"] == project_parameters["Название"]:
            not_in_project_name_data = False
            print("Данные проекта внесены")
            option = input(f"Выберите действие:\nПосмотреть данные\nИзменить данные\nРасчитать стоимость работ\n")

            if option == "Посмотреть данные":
                option_functions.print_dictionary_lines(project_parameters)
                open_project(project_name_data)

            elif option == "Изменить данные":
                option_functions.change_project_parameters(project_name_data, project_parameters)
                open_project(project_name_data)

            elif option == "Расчитать стоимость работ":
                estimate_dictionary = calculate_estimate.calculate_estimate(project_parameters)
                option_functions.print_dictionary_lines(estimate_dictionary)
                open_project(project_name_data)

    if not_in_project_name_data:
        option = input(f"Выберите действие:\nВнести данные?Да/Нет\n")
        if option == "Да":
            option_functions.create_project_parameters(project_name_data, parameters.project_parameters)
