from src import option_functions

from src import parameters


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

