from PyQt5 import QtWidgets

import numpy as np

from MapWindow import MapWindow
from Warning import WarningWindow


class GuillotineCuts:
    def __init__(self, main_sheet, details, details_square, details_count, first_orient, first_cut, cell):
        self.main_sheet = {  # главный лист
            'x': 0,  # положение левого нижнего угла листа на оси Х
            'y': 0,  # положение левого нижнего угла листа на оси Y
            'a': main_sheet['a'],  # длина листа
            'b': main_sheet['b'],  # ширина листа
            'ref_id': None,  # путем разрезания какого листа получен
            'det': None,
            # если является деталью, то id этой детали: int - id детали, None - неиспользованный лист, 'n' - отход
            'cut': None,  # разрез, который производится на данном листе: 0 - горизонтальный, 1 - вертикальный
            'm': None  # отступ при разрезе
        }

        self.main_sheet_square = main_sheet['a'] * main_sheet['b']  # площадь главного листа
        self.res = [self.main_sheet]  # список, с которым в дальнейшем будет идти работа
        # список, в котором будут содеражаться детали
        self.details = sorted(details, key=lambda item: (-item['a'] * item['b'], -item['a']))
        self.details_square = details_square  # общая площадь деталей
        self.details_count = details_count  # общее количество деталей
        self.waste_square = 0  # площадь отходов
        self.first_orient = first_orient  # первое проверяемое расположение детали: 0 - горизонтальное, 1 - вертикальное
        self.first_cut = first_cut  # первый проверяемый разрез: 0 - горизонтальный, 1 - вертикальный
        self.cell = cell

    def get_details(self):
        """
        Считываем из файла главный лист, на котором необходимо будет размесить детали, и сами детали
        :return: 
        """
        f = open('details.txt', 'r')  # открытие файла с деталями для чтения
        # считываем длину и ширину главного листа
        l = f.readline().split()
        self.main_sheet['a'] = int(l[0])
        self.main_sheet['b'] = int(l[1])
        # далее идем по файлу и счытываем детали, попутно считая их общую площадь и количество
        for line in f:
            s = line.split()
            self.details.append({
                'sum': int(s[0]),
                'a': int(s[1]),
                'b': int(s[2]),
                'or': int(s[3]) if len(s) == 4 else None
            })
            self.details_square += int(s[0]) * int(s[1]) * int(s[2])
            self.details_count += int(s[0])
        self.details = sorted(self.details, key=lambda item: (-item['a'] * item['b'], -item['a']))

    def recursive(self):
        sheets = self.get_sheets(self.res)  # получаем доступные для разрезания листы
        # если список листов не пустой, то берем последний из него
        # если деталей в этом же случае не осталось, то возвращаем True
        # если список листов пуст и деталей осталось больше 0, то возвращаем False
        sheet = sheets[-1] if len(sheets) > 0 else False if self.details_count > 0 else True
        if not isinstance(sheet, bool):
            result = False  # можно ли из этого листа вырезать деталь,
            # и будет ли результат положительным при дальнейшем рекурсивном выполнении
            for detail in self.details:
                if detail['sum'] == 0:
                    continue  # если деталей такого размера не осталось, переходим к следующему размеру
                if (self.get_orient(sheet, detail, True) and self.get_cut(sheet, detail)) or \
                        (self.get_orient(sheet, detail, False) and self.get_cut(sheet, detail)):
                    result = True
                    break
            if not result:
                # если из этого листа невозможно вырезать ни одну деталь из оставшихся, то помечаем ее, как отход
                sheet_square = sheet['a'] * sheet['b']
                if self.waste_square + sheet_square > self.available_waste_square:
                    # в случае превышения допустимой площади отходов откатываемся назад
                    return False
                else:
                    # если допустимая площадь отходов не превышается, увеличиваем ее и снова запускаем рекурсию
                    self.waste_square += sheet_square
                    sheet['det'] = 'n'
                    return self.recursive()
        else:
            return sheet
        return True

    def get_orient(self, sheet, detail, first):
        if first:
            return self.place_vertical(sheet, detail) if self.first_orient == 1 else self.place_horizontal(sheet,
                                                                                                           detail)
        else:
            return self.place_horizontal(sheet, detail) if self.first_orient == 1 else self.place_vertical(sheet,
                                                                                                           detail)

    def get_cut(self, sheet, detail, cur_cut=None):
        if cur_cut is None:
            return self.cut_vertical(sheet, detail) if self.first_cut == 1 else self.cut_horizontal(sheet, detail)
        elif cur_cut:
            return self.cut_horizontal(sheet, detail) if self.first_cut == cur_cut else self.is_detail(sheet, detail)
        else:
            return self.cut_vertical(sheet, detail) if self.first_cut == cur_cut else self.is_detail(sheet, detail)

    @staticmethod
    def get_sheets(act_list):
        """
        Получаем список доступных для разрезания листов
        :param act_list: основной список, с которым ведется работа 
        :return: спиоск объектов из основного листа, которые не являются деталями и не были подвергнуты разрезанию
        """
        return [item for item in act_list if item['det'] is None and item['cut'] is None]

    @staticmethod
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

    @staticmethod
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

    def is_detail(self, sheet, detail):
        """
        Проверка на то, является ли данный лист деталью
        :param sheet: лист
        :param detail: деталь
        :return:    
        True - с данным расположением детали дальнейшее рекурсивное выполнение было положительным
        False - лист не является деталью 
        или с данным расположением дальнейшее рекрсивное выполнение было отрицательным
        """
        if sheet['a'] == detail['a'] and sheet['b'] == detail['b']:
            sheet['det'] = self.details.index(detail)
            detail['sum'] -= 1
            self.details_count -= 1
            if not self.recursive():
                # если дальнейшее рекурсивное выполнение дает отрицательный результат,
                # то возвращаем те значения, что были до его выполнения
                if detail['a'] < detail['b']:
                    detail['a'], detail['b'] = detail['b'], detail['a']
                detail['sum'] += 1
                self.details_count += 1
                return False
            return True
        return False

    def cut_horizontal(self, sheet, detail):
        """
        Попытка горизонтального разреза и дальнейшее рекурсивное выполнение 
        :param sheet: лист, на котором производится разрез
        :param detail: деталь, которую нужно вырезать
        :return: 
        True - в результате разреза листа, дальнейшее рекурсивное выполнение было положительным, или он оказался деталью
        False - в результате разреза листа, дальнейшее рекурсивное выполнение было отрицательным
        """
        if sheet['b'] == detail['b']:
            if self.first_cut == 0:
                return self.cut_vertical(sheet, detail)
            return self.is_detail(sheet, detail)
        sheet['cut'] = 0
        sheet['m'] = detail['b']
        new_sheet_1 = {
            'x': sheet['x'],
            'y': sheet['y'],
            'a': sheet['a'],
            'b': detail['b'],
            'ref_id': self.res.index(sheet),
            'det': None,
            'cut': None
        }
        new_sheet_2 = {
            'x': sheet['x'],
            'y': sheet['y'] + detail['b'],
            'a': sheet['a'],
            'b': sheet['b'] - detail['b'],
            'ref_id': self.res.index(sheet),
            'det': None,
            'cut': None
        }
        self.res.append(new_sheet_2)
        self.res.append(new_sheet_1)
        if not self.get_cut(self.res[-1], detail, 0):
            # если после рекурсивного выполнения с данным разрезом получен отрицательный результат,
            # то возвращаем те значения, что были до его выполнения
            for x in range(2):
                last_record = self.res.pop()
                if last_record['det'] == 'n':
                    self.waste_square -= last_record['a'] * last_record['b']
            return False
        return True

    def cut_vertical(self, sheet, detail):
        """
        Попытка вертикального разреза и дальнейшее рекурсивное выполнение 
        :param sheet: лист, на котором производится разрез
        :param detail: деталь, которую нужно вырезать
        :return: 
        True - в результате разреза листа, дальнейшее рекурсивное выполнение было положительным, или он оказался деталью
        False - в результате разреза листа, дальнейшее рекурсивное выполнение было отрицательным
        """
        if sheet['a'] == detail['a']:
            if self.first_cut == 1:
                return self.cut_horizontal(sheet, detail)
            return self.is_detail(sheet, detail)
        sheet['cut'] = 1
        sheet['m'] = detail['a']
        new_sheet_1 = {
            'x': sheet['x'],
            'y': sheet['y'],
            'a': detail['a'],
            'b': sheet['b'],
            'ref_id': self.res.index(sheet),
            'det': None,
            'cut': None
        }
        new_sheet_2 = {
            'x': sheet['x'] + detail['a'],
            'y': sheet['y'],
            'a': sheet['a'] - detail['a'],
            'b': sheet['b'],
            'ref_id': self.res.index(sheet),
            'det': None,
            'cut': None
        }
        self.res.append(new_sheet_2)
        self.res.append(new_sheet_1)
        if not self.get_cut(self.res[-1], detail, 1):
            # если после рекурсивного выполнения с данным разрезом получен отрицательный результат,
            # то возвращаем те значения, что были до его выполнения
            for x in range(2):
                last_record = self.res.pop()
                if last_record['det'] == 'n':
                    self.waste_square -= last_record['a'] * last_record['b']
            return False
        return True

    @staticmethod
    def warning():
        Dialog = QtWidgets.QDialog()
        ui = WarningWindow()
        ui.setupUi(Dialog)
        Dialog.show()
        Dialog.exec()

    def start_process(self):
        if self.main_sheet_square < self.details_square:
            self.warning()
        else:
            max_width = self.main_sheet['a']
            self.main_sheet['a'] = int(np.ceil(self.details_square / self.main_sheet['b']))
            self.available_waste_square = self.main_sheet['a'] * self.main_sheet['b'] - self.details_square
            self.main_sheet_square = self.main_sheet['a'] * self.main_sheet['b']
            while True:
                if self.recursive():
                    for i in range(len(self.res)):
                        print(i, self.res[i])
                    Dialog = QtWidgets.QDialog()
                    ui = MapWindow()
                    ui.setupUi(Dialog, self.res, self.cell)
                    Dialog.show()
                    Dialog.exec()
                    break
                elif self.main_sheet['a'] < max_width:
                    self.main_sheet['a'] += 1
                    self.main_sheet['cut'] = None
                    self.main_sheet['m'] = None
                    self.available_waste_square = self.main_sheet['a'] * self.main_sheet['b'] - self.details_square
                    self.main_sheet_square = self.main_sheet['a'] * self.main_sheet['b']
                else:
                    self.warning()
                    self.res = [self.main_sheet]
                    break
