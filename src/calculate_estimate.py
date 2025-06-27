import parameters

import copy


def calculate_estimate(project_parameters):
    """
    Функция создает смету из параметров проекта

    Запись параметров сметы в словарь:: осуществляется путем составления из разных параметров проекта

    Расчет количества отверстий под подрозетники:: складывание количества розеток и выключателей

    Расчет количества штробы:: путем составления умножения количества розеток и выключателей на соответствующие
    коэффициенты, полученные эмпирическим путем !!!!! Требует пересмотра !!!!!

    Расчет количества кабеля:: путем составления умножения количества розеток на соответствующее количество и
    дополнительных линий на приборы. Полученный результат умножается на коэффициент, полученные путем учета различных
    параметров объекта !!!!! Требует доработки !!!!!

    Расчет количества монтируемых подрозетников:: с количества отверстий под подрозетники

    Замена вводного кабеля:: добавляется в зависимости соответствующего от параметра объекта

    Расчет количества автоматов для щита:: часть функции для определения количества автоматов с учетом типа проекта
    и определения типоразмера щита

    Устройство ниши под щит:: добавляется в зависимости соответствующего от параметра объекта

    """

    # Создаем словарь для записи пунктов сметы
    project_estimate = {}

    # Запись параметров сметы в словарь
    project_estimate["Название проекта"] = project_parameters["Название"]
    project_estimate["Список работ"] = "До замера"
    project_estimate["Объект:"] = f"{project_parameters["Тип проекта"]}, {project_parameters["Площадь помещения"]}м2"

    # Расчет количества отверстий под подрозетники:
    socket_key = f"Устройство отверстия под подрозетник ({project_parameters["Материал стен"].lower()})"
    socket_count = (
        int(project_parameters["Количество розеток"])
        + int(project_parameters["Количество выключателей"])
        + int(project_parameters["Количество розеток слаботочных"])
    )
    socket_price = socket_count * parameters.price_list[socket_key]
    # Записываем позицию в смету по параметрам: количество, тариф, стоимость
    if project_parameters["Материал стен"].lower() == project_parameters["Материал перегородок"].lower():
        project_estimate[socket_key] = f"{socket_count}шт * {parameters.price_list[socket_key]} = {socket_price}руб."
    else:
        project_estimate[socket_key] = (
            f"{round(socket_count * 0.7)}шт * {parameters.price_list[socket_key]} = "
            f"{round(socket_count * 0.7) * parameters.price_list[socket_key]}руб."
        )
        socket_key = f"Устройство отверстия под подрозетник ({project_parameters["Материал перегородок"].lower()})"
        project_estimate[socket_key] = (
            f"{round(socket_count * 0.3)}шт * {parameters.price_list[socket_key]} = "
            f"{round(socket_count * 0.3) * parameters.price_list[socket_key]}руб."
        )

    # Расчет количества штробы:
    groove_coefficient = 1
    if project_parameters["Потолки Штукатурно-малярные(Да)/подвесные(Нет)"] == "Да":
        groove_coefficient *= 2
    if int(project_parameters["Площадь помещения"]) > 80:
        groove_coefficient *= 1.2
    if int(project_parameters["Площадь помещения"]) > 140:
        groove_coefficient *= 1.2
    if project_parameters["Тип проекта"] == "дом" or project_parameters["Тип проекта"] == "коммерция":
        groove_coefficient *= 1.2
    print(groove_coefficient)
    groove_count = round(
        (
            int(project_parameters["Количество розеток"]) * 1.2
            + int(project_parameters["Количество выключателей"]) * 1.5
            + int(project_parameters["Количество розеток слаботочных"]) * 1.5
        )
        * groove_coefficient
    )
    print(groove_count)
    if project_parameters["Материал стен"].lower() != "гипсокартон":
        groove_key = f"Штробление стен 20*20 ({project_parameters["Материал стен"].lower()})"
        groove_price = groove_count * parameters.price_list[groove_key]
        # Записываем позицию в смету по параметрам: количество, тариф, стоимость
        if project_parameters["Материал стен"].lower() == project_parameters["Материал перегородок"].lower():
            project_estimate[groove_key] = (
                f"{groove_count}м.п. * {parameters.price_list[groove_key]} = {groove_price}руб"
            )
        else:
            project_estimate[groove_key] = (
                f"{round(groove_count * 0.7)}м.п. * {parameters.price_list[groove_key]} = "
                f"{round(groove_count * 0.7) * parameters.price_list[groove_key]}руб"
            )
            if (
                project_parameters["Материал перегородок"].lower() != "Гипсокартон"
                and project_parameters["Материал стен"].lower() != project_parameters["Материал перегородок"].lower()
            ):
                groove_key = f"Штробление стен 20*20 ({project_parameters["Материал перегородок"].lower()})"
                project_estimate[groove_key] = (
                    f"{round(groove_count * 0.3)}м.п. * {parameters.price_list[groove_key]} = "
                    f"{round(groove_count * 0.3) * parameters.price_list[groove_key]}руб"
                )

    # Расчет количества кабеля:
    cable_coefficient = 1
    if project_parameters["Потолки Штукатурно-малярные(Да)/подвесные(Нет)"] == "Да":
        cable_coefficient *= 1.2
    if int(project_parameters["Площадь помещения"]) > 80:
        cable_coefficient *= 1.2
    if int(project_parameters["Площадь помещения"]) > 140:
        cable_coefficient *= 1.2
    if project_parameters["Тип проекта"] == "дом" or project_parameters["Тип проекта"] == "коммерция":
        cable_coefficient *= 1.2
    # 5*2,5 / 3*6
    cable_count = 0
    if project_parameters["Приборы (электрическая плита)"] == "Да":
        cable_count += 15
    if project_parameters["Приборы (водонагреватель)"] == "Да":
        cable_count += 15
    if cable_count != 0:
        cable_count *= cable_coefficient
        project_estimate["Протяжка кабеля силового 3*6.0 / 5*2.5"] = (
            f"{round(cable_count)}м.п. * {parameters.price_list["Протяжка кабеля силового 3*6.0 / 5*2.5"]} = "
            f"{round(cable_count) * parameters.price_list["Протяжка кабеля силового 3*6.0 / 5*2.5"]}руб"
        )
    # 3*2,5
    cable_for_socket_coefficient = cable_coefficient
    if (int(project_parameters["Количество розеток"]) / int(project_parameters["Площадь помещения"])) > 1.4:
        cable_for_socket_coefficient = cable_coefficient * 1.4
    cable_count = int(project_parameters["Количество комнат"]) * 30
    if project_parameters["Приборы (стиральная машина)"] == "Да":
        cable_count += 10
    if project_parameters["Приборы (посудомоечная машина)"] == "Да":
        cable_count += 10
    if project_parameters["Приборы (бойлер)"] == "Да":
        cable_count += 10
    if project_parameters["Приборы (Духовой шкаф)"] == "Да":
        cable_count += 10

    cable_count += int(project_parameters["Приборы (дополнительно)"]) * 10
    print(cable_count)
    cable_count *= cable_for_socket_coefficient

    project_estimate["Протяжка кабеля силового 3*2.5"] = (
        f"{round(cable_count, -1)}м.п. * {parameters.price_list["Протяжка кабеля силового 3*2.5"]} = "
        f"{round(cable_count, -1) * parameters.price_list["Протяжка кабеля силового 3*2.5"]}руб"
    )
    # 3*1,5
    cable_for_light_coefficient = cable_coefficient
    if (int(project_parameters["Количество точек освещения"]) / int(project_parameters["Количество комнат"])) > 2:
        cable_for_light_coefficient = cable_coefficient * 1.4
    if (int(project_parameters["Количество выключателей"]) / int(project_parameters["Количество комнат"])) > 2.5:
        cable_for_light_coefficient = cable_coefficient * 1.4
    cable_count = int(project_parameters["Количество комнат"]) * 20 * cable_for_light_coefficient
    project_estimate["Протяжка кабеля силового 3*1.5"] = (
        f"{round(cable_count, -1)}м.п. * {parameters.price_list["Протяжка кабеля силового 3*1.5"]} = "
        f"{round(cable_count, -1) * parameters.price_list["Протяжка кабеля силового 3*1.5"]}руб"
    )

    # Расчет количества монтируемых подрозетников:
    project_estimate["Монтаж подрозетника"] = (
        f"{socket_count}шт * {parameters.price_list["Монтаж подрозетника"]} = "
        f"{socket_count * parameters.price_list["Монтаж подрозетника"]}руб."
    )

    # Расчет количества отверстий:

    # Замена вводного кабеля:
    if project_parameters["Нужна замена вводного кабеля в квартиру"] == "Да":
        project_estimate["Замена вводного кабеля"] = (
            f" 1шт * {parameters.price_list["Замена вводного кабеля"]} = "
            f"{parameters.price_list["Замена вводного кабеля"]}руб."
        )

    # Расчет количества автоматов для щита:
    module_counter = 0
    circuit_breakers_project_list = copy.deepcopy(parameters.circuit_breakers_list)

    if project_parameters["Тип проекта"] == "дом":
        circuit_breakers_project_list["Рубильник реверсивный"] = 1
        module_counter += 4
        circuit_breakers_project_list["Вводное УЗО"] = 1
        module_counter += 4
        circuit_breakers_project_list["Влагозащитное УЗО"] = 2
        module_counter += 4
        circuit_breakers_project_list["Уличное УЗО"] = 1
        module_counter += 2
        circuit_breakers_project_list["Автомат большой мощности"] = sum(
            [
                project_parameters["Приборы (электрическая плита)"] == "Да",
                project_parameters["Приборы (водонагреватель)"] == "Да",
            ]
        )
        module_counter += 3 * circuit_breakers_project_list["Автомат большой мощности"]

    elif project_parameters["Тип проекта"] == "квартира":
        circuit_breakers_project_list["Рубильник реверсивный"] = 0
        circuit_breakers_project_list["Вводное УЗО"] = 1
        module_counter += 2
        circuit_breakers_project_list["Влагозащитное УЗО"] = 1
        module_counter += 2
        circuit_breakers_project_list["Уличное УЗО"] = 0
        circuit_breakers_project_list["Автомат большой мощности"] = sum(
            [
                project_parameters["Приборы (электрическая плита)"] == "Да",
                project_parameters["Приборы (водонагреватель)"] == "Да",
            ]
        )
        module_counter += circuit_breakers_project_list["Автомат большой мощности"]

    circuit_breakers_project_list["Дифференциальный автомат 16А 30мА"] = sum(
        [
            project_parameters["Приборы (стиральная машина)"] == "Да",
            project_parameters["Приборы (посудомоечная машина)"] == "Да",
            project_parameters["Приборы (бойлер)"] == "Да",
        ]
    )
    module_counter += 2 * circuit_breakers_project_list["Дифференциальный автомат 16А 30мА"]

    circuit_breakers_project_list["Автомат 16А"] = sum(
        [
            int(project_parameters["Количество комнат"]) + 1,
            project_parameters["Приборы (Духовой шкаф)"] == "Да",
            int(project_parameters["Приборы (дополнительно)"]),
        ]
    )
    module_counter += circuit_breakers_project_list["Автомат 16А"]

    circuit_breakers_project_list["Автомат 10А"] = (int(project_parameters["Количество комнат"]) + 1) // 2
    module_counter += circuit_breakers_project_list["Автомат 10А"]

    if project_parameters["Тип проекта"] == "частичная (комната/кухня)":
        project_estimate["Количество дополнительных автоматов"] = "По результатам замера"
    else:
        switch_box_modules = (module_counter // 12 + 1) * 12 if module_counter < 48 else 48
        switch_box_key = f"Монтаж, сборка и подключение щита силового ({switch_box_modules}мод)"
        project_estimate[switch_box_key] = (
            f"1шт * {parameters.price_list[switch_box_key]} = " f"{parameters.price_list[switch_box_key]} руб."
        )

        # Устройство ниши под щит:
        if project_parameters["Щит"] == "Встроенный":
            switch_box_key = f"Устройство ниши под щит ({switch_box_modules}мод)"
            project_estimate[switch_box_key] = (
                f" 1шт * {parameters.price_list[switch_box_key]} = " f"{parameters.price_list[switch_box_key]}руб."
            )

    return project_estimate
