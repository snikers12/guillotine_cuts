import sys

main_sheet = {
    'x': 0,
    'y': 0,
    'a': 52,
    'b': 25,
    'ref_id': None,
    'det': None,
    'cut': None,
    'm': None
}

main_sheet_square = main_sheet['a'] * main_sheet['b']
res = [main_sheet]
details = list()
details_square = 0
details_count = 0
rubber_square = 0
sys.setrecursionlimit(1500)


def get_details():
    f = open('details.txt', 'r')
    global details_square
    global details_count
    for line in f:
        s = line.split()
        details.append({
            'sum': int(s[0]),
            'a': int(s[1]),
            'b': int(s[2])
        })
        details_square += int(s[0]) * int(s[1]) * int(s[2])
        details_count += int(s[0])


def main():
    global rubber_square
    sheets = get_sheets(res)
    sheet = sheets[-1] if len(sheets) > 0 else False if details_count > 0 else True
    if not isinstance(sheet, bool):
        result = True
        for detail in details:
            if detail['sum'] == 0:
                continue
            else:
                result = False
            if (place_vertical(sheet, detail) and cut_vertical(sheet, detail)) or \
                    (place_horizontal(sheet, detail) and cut_vertical(sheet, detail)):
                result = True
                break
        if not result:
            sheet_square = sheet['a'] * sheet['b']
            if rubber_square + sheet_square > available_rubber_square:
                return False
            else:
                rubber_square += sheet_square
                sheet['det'] = 'n'
                return main()
    return True


def get_sheets(act_list):
    return [item for item in act_list if item['det'] is None and item['cut'] is None]


def get_detail(details_list):
    if details_list:
        detail = details_list.pop(0)
        return detail
    else:
        return False


def place_horizontal(sheet, detail):
    if sheet['a'] < detail['a'] or sheet['b'] < detail['b']:
        return False
    return True


def place_vertical(sheet, detail):
    if sheet['b'] < detail['a'] or sheet['a'] < detail['b']:
        return False
    detail['a'], detail['b'] = detail['b'], detail['a']
    return True


def is_detail(sheet, detail):
    global rubber_square
    if sheet['a'] == detail['a'] and sheet['b'] == detail['b']:
        sheet['det'] = details.index(detail)
        detail['sum'] -= 1
        if not main():
            if detail['a'] < detail['b']:
                detail['a'], detail['b'] = detail['b'], detail['a']
            detail['sum'] += 1
            return False
        return True
    return False


def cut_horizontal(sheet, detail):
    global rubber_square
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
        for x in range(2):
            last_record = res.pop()
            if last_record['det'] == 'n':
                rubber_square -= last_record['a'] * last_record['b']
        return False
    return True


def cut_vertical(sheet, detail):
    global rubber_square
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
        for x in range(2):
            last_record = res.pop()
            if last_record['det'] == 'n':
                rubber_square -= last_record['a'] * last_record['b']
        return False
    return True


get_details()
available_rubber_square = main_sheet['a'] * main_sheet['b'] - details_square
can_be_placed = main()
if can_be_placed:
    for i in range(len(res)):
        print(i, res[i])
else:
    print(False)
