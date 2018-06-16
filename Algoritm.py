import sys
import numpy as np
from PyQt5.QtWidgets import QApplication
from qtpy import QtWidgets

from MapWindow import MapWindow
from Painting import Painting
import math
import time

main_sheet = {  # главный лист
    'x': 0,  # положение левого нижнего угла листа на оси Х
    'y': 0,  # положение левого нижнего угла листа на оси Y
    'a': 0,  # длина листа
    'b': 0,  # ширина листа
}

main_sheet_square = 0  # площадь главного листа
res = [main_sheet]  # список, с которым в дальнейшем будет идти работа
details = list()  # список, в котором будут содеражаться детали
details_square = 0  # общая площадь деталей
details_count = 0  # общее количество деталей
waste_square = 0  # площадь отходов
min_length = 0
min_width = 0


def get_details():
    """
    Считываем из файла главный лист, на котором необходимо будет размесить детали, и сами детали
    :return: 
    """
    f = open('details1.txt', 'r')  # открытие файла с деталями для чтения
    global details_square, details_count, main_sheet_square, details, min_width, min_length
    # считываем длину и ширину главного листа
    l = f.readline().split()
    main_sheet['a'] = int(l[0])
    main_sheet['b'] = int(l[1])
    main_sheet_square = main_sheet['a'] * main_sheet['b']  # площадь главного листа
    # далее идем по файлу и счытываем детали, попутно считая их общую площадь и количество
    for line in f:
        s = line.split()
        detail_count = int(s[0])
        detail_length = int(s[1])
        detail_width = int(s[2])
        orientation = int(s[3]) if len(s) == 4 else None
        if detail_length < detail_width:
            detail_length, detail_width = detail_width, detail_length
        details.append({
            'sum': detail_count,
            'a': detail_length,
            'b': detail_width,
            'or': orientation
        })
        min_length = detail_length if orientation == 0 and detail_length > min_length else detail_width if \
            detail_width > min_length else min_length
        min_width = detail_width if orientation == 1 and detail_width > min_width else detail_length if \
            detail_length > min_width else min_width
        details_square += detail_count * detail_length * detail_width
        details_count += detail_count
    details = sorted(details, key=lambda item: (-item['a']*item['b'], -item['a']))


def recursive():
    global waste_square
    sheets = sorted(get_sheets(res), key=lambda item: (item['a']*item['b']))
    # получаем доступные для разрезания листы
    # если список листов не пустой, то берем последний из него
    # если деталей в этом же случае не осталось, то возвращаем True
    # если список листов пуст и деталей осталось больше 0, то возвращаем False
    sheet = sheets[0] if len(sheets) > 0 else False if details_count > 0 else True
    if not isinstance(sheet, bool):
        result = False  # можно ли из этого листа вырезать деталь,
        # и будет ли результат положительным при дальнейшем рекурсивном выполнении
        for detail in details:
            if detail['sum'] == 0:
                continue  # если деталей такого размера не осталось, переходим к следующему размеру
            if (get_orient(sheet, detail, True) and get_cut(sheet, detail, True)) or \
                    (get_orient(sheet, detail, True) and get_cut(sheet, detail, False)) or \
                    (get_orient(sheet, detail, False) and get_cut(sheet, detail, True)) or \
                    (get_orient(sheet, detail, False) and get_cut(sheet, detail, False)):
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
                sheet['det'] = False
                return recursive()
    else:
        return sheet
    return True


def get_orient(sheet, detail, first):
    if first:
        return place_vertical(sheet, detail) if sheet['a'] >= sheet['b'] else place_horizontal(sheet, detail)
    else:
        return place_horizontal(sheet, detail) if sheet['a'] >= sheet['b'] else place_vertical(sheet, detail)


def get_cut(sheet, detail, first):
    if first:
        return cut_vertical(sheet, detail, True) if sheet['b'] - detail['b'] < sheet['a'] - detail['a'] \
            else cut_horizontal(sheet, detail, True)
    else:
        return cut_horizontal(sheet, detail, True) if sheet['b'] - detail['b'] < sheet['a'] - detail['a'] \
            else cut_vertical(sheet, detail, True)


def get_sheets(act_list):
    """
    Получаем список доступных для разрезания листов
    :param act_list: основной список, с которым ведется работа 
    :return: список объектов из основного листа, которые не являются деталями и не были подвергнуты разрезанию
    """
    return [item for item in act_list if item.get('det') is None and item.get('cut') is None]


def place_horizontal(sheet, detail):
    """
    Попытка расположить деталь горизонтально
    :param sheet: лист, на котором идет расположение детали 
    :param detail: деталь
    :return:    
    True - деталь можно расположить горизонтально
    False - деталь нельзя расположить горизонтально
    """
    if detail['a'] < detail['b']:
        detail['a'], detail['b'] = detail['b'], detail['a']
    if sheet['a'] < detail['a'] or sheet['b'] < detail['b'] or detail['or'] == 1:
        return False
    return True


def place_vertical(sheet, detail):
    """
    Попытка расположить деталь вертикльно
    :param sheet: лист, на котором идет расположение детали 
    :param detail: деталь
    :return:    
    True - деталь можно расположить вертикально
    False - деталь нельзя расположить вертикально
    """
    if detail['a'] > detail['b']:
        detail['a'], detail['b'] = detail['b'], detail['a']
    if sheet['a'] < detail['a'] or sheet['b'] < detail['b'] or detail['or'] == 0:
        return False
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
        sheet['det'] = True
        detail['sum'] -= 1
        details_count -= 1
        if not recursive():
            # если дальнейшее рекурсивное выполнение дает отрицательный результат,
            # то возвращаем те значения, что были до его выполнения
            detail['sum'] += 1
            details_count += 1
            return False
        return True
    return False


def cut_horizontal(sheet, detail, first):
    """
    Попытка горизонтального разреза и дальнейшее рекурсивное выполнение 
    :param first: является ли этот разрез первым
    :param sheet: лист, на котором производится разрез
    :param detail: деталь, которую нужно вырезать
    :return: 
    True - в результате разреза листа, дальнейшее рекурсивное выполнение было положительным, или он оказался деталью
    False - в результате разреза листа, дальнейшее рекурсивное выполнение было отрицательным
    """
    global waste_square
    if sheet['b'] == detail['b']:
        if first:
            return cut_vertical(sheet, detail, False)
        return is_detail(sheet, detail)
    sheet['cut'] = 0
    sheet['m'] = detail['b']
    new_sheet_1 = {
        'x': sheet['x'],
        'y': sheet['y'],
        'a': sheet['a'],
        'b': detail['b'],
    }
    new_sheet_2 = {
        'x': sheet['x'],
        'y': sheet['y'] + detail['b'],
        'a': sheet['a'],
        'b': sheet['b'] - detail['b'],
    }
    res.append(new_sheet_2)
    res.append(new_sheet_1)
    if not cut_vertical(res[-1], detail, False):
        # если после рекурсивного выполнения с данным разрезом получен отрицательный результат,
        # то возвращаем те значения, что были до его выполнения
        for x in range(2):
            last_record = res.pop()
            if last_record.get('det') is False:
                waste_square -= last_record['a'] * last_record['b']
        return False
    return True


def cut_vertical(sheet, detail, first):
    """
    Попытка вертикального разреза и дальнейшее рекурсивное выполнение 
    :param first: является ли этот разрез первым
    :param sheet: лист, на котором производится разрез
    :param detail: деталь, которую нужно вырезать
    :return: 
    True - в результате разреза листа, дальнейшее рекурсивное выполнение было положительным, или он оказался деталью
    False - в результате разреза листа, дальнейшее рекурсивное выполнение было отрицательным
    """
    global waste_square
    if sheet['a'] == detail['a']:
        if first:
            return cut_horizontal(sheet, detail, False)
        return is_detail(sheet, detail)
    sheet['cut'] = 1
    sheet['m'] = detail['a']
    new_sheet_1 = {
        'x': sheet['x'],
        'y': sheet['y'],
        'a': detail['a'],
        'b': sheet['b'],
    }
    new_sheet_2 = {
        'x': sheet['x'] + detail['a'],
        'y': sheet['y'],
        'a': sheet['a'] - detail['a'],
        'b': sheet['b'],
    }
    res.append(new_sheet_2)
    res.append(new_sheet_1)
    if not cut_horizontal(res[-1], detail, False):
        # если после рекурсивного выполнения с данным разрезом получен отрицательный результат,
        # то возвращаем те значения, что были до его выполнения
        for x in range(2):
            last_record = res.pop()
            if last_record.get('det') is False:
                waste_square -= last_record['a'] * last_record['b']
        return False
    return True


if __name__ == '__main__':
    get_details()
    if main_sheet_square < details_square:
        print("Can't be placed!")
    else:
        start_time = time.time()
        max_length = main_sheet['a']
        max_width = main_sheet['b']
        max_square = details_square
        while max_square < max_length * max_width:
            i = max_width
            checked = []
            while i >= min_width:
                if max_square % i != 0 or i in checked:
                    i -= 1
                    continue
                if max_length >= (max_square//i) >= min_length and max_width >= i >= min_width:
                    checked += [i, max_square//i]
                    main_sheet['a'] = max_square // i
                    main_sheet['b'] = i
                    cur_length = main_sheet['a']
                    cur_width = main_sheet['b']
                    available_waste_square = main_sheet['a'] * main_sheet['b'] - details_square
                    main_sheet_square = main_sheet['a'] * main_sheet['b']
                    main_sheet['cut'] = None
                    if recursive():
                        for i in range(len(res)):
                            print(i, res[i])
                        print(time.time()-start_time)
                        app = QtWidgets.QApplication(sys.argv)
                        Dialog = QtWidgets.QDialog()
                        ui = MapWindow()
                        ui.setupUi(Dialog, res, 20)
                        Dialog.show()
                        Dialog.exec()
                        sys.exit(app.exec_())
                if max_width >= (max_square//i) >= min_width and max_length >= i >= min_length:
                    checked += [i, max_square//i]
                    main_sheet['a'] = i
                    main_sheet['b'] = max_square // i
                    cur_length = main_sheet['a']
                    cur_width = main_sheet['b']
                    available_waste_square = main_sheet['a'] * main_sheet['b'] - details_square
                    main_sheet_square = main_sheet['a'] * main_sheet['b']
                    main_sheet['cut'] = None
                    if recursive():
                        for i in range(len(res)):
                            print(i, res[i])
                        print(time.time()-start_time)
                        app = QtWidgets.QApplication(sys.argv)
                        Dialog = QtWidgets.QDialog()
                        ui = MapWindow()
                        ui.setupUi(Dialog, res, 20)
                        Dialog.show()
                        Dialog.exec()
                        sys.exit(app.exec_())
                i -= 1
            max_square += 1
        print("Can't be placed!")
