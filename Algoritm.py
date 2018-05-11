import sys
import numpy as np
from PyQt5.QtWidgets import QApplication

from Painting import Painting

main_sheet = {  # главный лист
    'x': 0,  # положение левого нижнего угла листа на оси Х
    'y': 0,  # положение левого нижнего угла листа на оси Y
    'a': 0,  # длина листа
    'b': 0,  # ширина листа
    'ref_id': None,  # путем разрезания какого листа получен
    'det': None,  # если является деталью, то id этой детали: int - id детали, None - неиспользованный лист, 'n' - отход
    'cut': None,  # разрез, который производится на данном листе: 0 - горизонтальный, 1 - вертикальный
    'm': None  # отступ при разрезе
}

main_sheet_square = 0  # площадь главного листа
res = [main_sheet]  # список, с которым в дальнейшем будет идти работа
details = list()  # список, в котором будут содеражаться детали
details_square = 0  # общая площадь деталей
details_count = 0  # общее количество деталей
waste_square = 0  # площадь отходов


def get_details():
    """
    Считываем из файла главный лист, на котором необходимо будет размесить детали, и сами детали
    :return: 
    """
    f = open('details.txt', 'r')  # открытие файла с деталями для чтения
    global details_square, details_count, main_sheet_square, details
    # считываем длину и ширину главного листа
    l = f.readline().split()
    main_sheet['a'] = int(l[0])
    main_sheet['b'] = int(l[1])
    main_sheet_square = main_sheet['a'] * main_sheet['b']
    # далее идем по файлу и счытываем детали, попутно считая их общую площадь и количество
    for line in f:
        s = line.split()
        details.append({
            'sum': int(s[0]),
            'a': int(s[1]),
            'b': int(s[2]),
            'or': int(s[3]) if len(s) == 4 else None
        })
        details_square += int(s[0]) * int(s[1]) * int(s[2])
        details_count += int(s[0])
    details = sorted(details, key=lambda item: (-item['a']*item['b'], -item['a']))


def recursive():
    global waste_square
    sheets = get_sheets(res)  # получаем доступные для разрезания листы
    # если список листов не пустой, то берем последний из него
    # если деталей в этом же случае не осталось, то возвращаем True
    # если список листов пуст и деталей осталось больше 0, то возвращаем False
    sheet = sheets[-1] if len(sheets) > 0 else False if details_count > 0 else True
    if not isinstance(sheet, bool):
        result = False  # можно ли из этого листа вырезать деталь,
        # и будет ли результат положительным при дальнейшем рекурсивном выполнении
        for detail in details:
            if detail['sum'] == 0:
                continue  # если деталей такого размера не осталось, переходим к следующему размеру
            if (place_vertical(sheet, detail) and cut_vertical(sheet, detail)) or \
                    (place_horizontal(sheet, detail) and cut_vertical(sheet, detail)):
                result = True
                break
        if not result:
            # если из этого листа невозможно вырезать ни одну деталь из оставшихся, то помечаем ее, как отход
            sheet_square = sheet['a'] * sheet['b']
            if waste_square + sheet_square > available_waste_square:
                # в случае превышения допустимой площади отходов откатываемся назад
                return False
            else:
                # если допустимая площадь отходов не превышается, увеличиваем ее и снова запускаем рекурсию
                waste_square += sheet_square
                sheet['det'] = 'n'
                return recursive()
    else:
        return sheet
    return True


def get_sheets(act_list):
    """
    Получаем список доступных для разрезания листов
    :param act_list: основной список, с которым ведется работа 
    :return: спиоск объектов из основного листа, которые не являются деталями и не были подвергнуты разрезанию
    """
    return [item for item in act_list if item['det'] is None and item['cut'] is None]


def place_horizontal(sheet, detail):
    """
    Попытка расположить деталь горизонтально
    :param sheet: лист, на котором идет расположение детали 
    :param detail: деталь
    :return:    
    True - деталь можно расположить горизонтально
    False - деталь нельзя расположить горизонтально
    """
    if sheet['a'] < detail['a'] or sheet['b'] < detail['b'] or detail['or'] == 1:
        return False
    return True


def place_vertical(sheet, detail):
    """
    Попытка расположить деталь вертикльно
    :param sheet: лист, на котором идет расположение детали 
    :param detail: деталь
    :return:    
    True - деталь можно расположить вертикльно
    False - деталь нельзя расположить вертикльно
    """
    if sheet['b'] < detail['a'] or sheet['a'] < detail['b'] or detail['or'] == 0:
        return False
    detail['a'], detail['b'] = detail['b'], detail['a']
    return True


def is_detail(sheet, detail):
    """
    Проверка на то, является ли данный лист деталью
    :param sheet: лист
    :param detail: деталь
    :return:    
    True - с данным расположением детали дальнейшее рекурсивное выполнение было положительным
    False - лист не является деталью 
    или с данным расположением дальнейшее рекрсивное выполнение было отрицательным
    """
    global details_count
    if sheet['a'] == detail['a'] and sheet['b'] == detail['b']:
        sheet['det'] = details.index(detail)
        detail['sum'] -= 1
        details_count -= 1
        if not recursive():
            # если дальнейшее рекурсивное выполнение дает отрицательный результат,
            # то возвращаем те значения, что были до его выполнения
            if detail['a'] < detail['b']:
                detail['a'], detail['b'] = detail['b'], detail['a']
            detail['sum'] += 1
            details_count += 1
            return False
        return True
    return False


def cut_horizontal(sheet, detail):
    """
    Попытка горизонтального разреза и дальнейшее рекурсивное выполнение 
    :param sheet: лист, на котором производится разрез
    :param detail: деталь, которую нужно вырезать
    :return: 
    True - в результате разреза листа, дальнейшее рекурсивное выполнение было положительным, или он оказался деталью
    False - в результате разреза листа, дальнейшее рекурсивное выполнение было отрицательным
    """
    global waste_square
    if sheet['b'] == detail['b']:
        return is_detail(sheet, detail)
    sheet['cut'] = 0
    sheet['m'] = detail['b']
    new_sheet_1 = {
        'x': sheet['x'],
        'y': sheet['y'],
        'a': sheet['a'],
        'b': detail['b'],
        'ref_id': res.index(sheet),
        'det': None,
        'cut': None
    }
    new_sheet_2 = {
        'x': sheet['x'],
        'y': sheet['y'] + detail['b'],
        'a': sheet['a'],
        'b': sheet['b'] - detail['b'],
        'ref_id': res.index(sheet),
        'det': None,
        'cut': None
    }
    res.append(new_sheet_2)
    res.append(new_sheet_1)
    if not is_detail(res[-1], detail):
        # если после рекурсивного выполнения с данным разрезом получен отрицательный результат,
        # то возвращаем те значения, что были до его выполнения
        for x in range(2):
            last_record = res.pop()
            if last_record['det'] == 'n':
                waste_square -= last_record['a'] * last_record['b']
        return False
    return True


def cut_vertical(sheet, detail):
    """
    Попытка вертикального разреза и дальнейшее рекурсивное выполнение 
    :param sheet: лист, на котором производится разрез
    :param detail: деталь, которую нужно вырезать
    :return: 
    True - в результате разреза листа, дальнейшее рекурсивное выполнение было положительным, или он оказался деталью
    False - в результате разреза листа, дальнейшее рекурсивное выполнение было отрицательным
    """
    global waste_square
    if sheet['a'] == detail['a']:
        return cut_horizontal(sheet, detail)
    sheet['cut'] = 1
    sheet['m'] = detail['a']
    new_sheet_1 = {
        'x': sheet['x'],
        'y': sheet['y'],
        'a': detail['a'],
        'b': sheet['b'],
        'ref_id': res.index(sheet),
        'det': None,
        'cut': None
    }
    new_sheet_2 = {
        'x': sheet['x'] + detail['a'],
        'y': sheet['y'],
        'a': sheet['a'] - detail['a'],
        'b': sheet['b'],
        'ref_id': res.index(sheet),
        'det': None,
        'cut': None
    }
    res.append(new_sheet_2)
    res.append(new_sheet_1)
    if not cut_horizontal(res[-1], detail):
        # если после рекурсивного выполнения с данным разрезом получен отрицательный результат,
        # то возвращаем те значения, что были до его выполнения
        for x in range(2):
            last_record = res.pop()
            if last_record['det'] == 'n':
                waste_square -= last_record['a'] * last_record['b']
        return False
    return True


if __name__ == '__main__':
    get_details()
    if main_sheet_square < details_square:
        print("Can't be placed!")
    else:
        max_width = main_sheet['a']
        main_sheet['a'] = int(np.ceil(details_square/main_sheet['b']))
        available_waste_square = main_sheet['a'] * main_sheet['b'] - details_square
        main_sheet_square = main_sheet['a'] * main_sheet['b']
        while True:
            if recursive():
                for i in range(len(res)):
                    print(i, res[i])
                app = QApplication(sys.argv)
                ex = Painting(res)
                sys.exit(app.exec_())
            elif main_sheet['a'] < max_width:
                main_sheet['a'] += 1
                available_waste_square = main_sheet['a'] * main_sheet['b'] - details_square
                main_sheet_square = main_sheet['a'] * main_sheet['b']
            else:
                print("Can't be placed!")
                break
