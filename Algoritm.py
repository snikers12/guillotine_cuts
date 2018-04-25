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
rubber_square = 0
sys.setrecursionlimit(1500)


def get_details():
    f = open('details.txt', 'r')
    global details_square
    for line in f:
        s = line.split()
        details.append({
            'sum': int(s[0]),
            'a': int(s[1]),
            'b': int(s[2])
        })
        details_square += int(s[0]) * int(s[1]) * int(s[2])


def main():
    global rubber_square
    dets = details
    sheets = get_sheet(res)
    for sheet in reversed(sheets):
        result = True
        for detail in dets:
            if detail['sum'] == 0:
                continue
            else:
                result = False
            if place_vertical(sheet, detail) or place_horizontal(sheet, detail):
                if cut_vertical(sheet, detail) or cut_horizontal(sheet, detail):
                    result = True
                    break
        if not result:
            sheet['det'] = 'n'
            sheet_square = sheet['a'] * sheet['b']
            if rubber_square == 51:
                rubber_square
            if rubber_square + sheet_square > available_rubber_square:
                return False
            else:
                rubber_square += sheet_square


def get_sheet(act_list):
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
    return is_detail(sheet, detail)


def place_vertical(sheet, detail):
    if sheet['b'] < detail['a'] or sheet['a'] < detail['b']:
        return False
    detail['a'], detail['b'] = detail['b'], detail['a']
    return is_detail(sheet, detail)


def is_detail(sheet, detail):
    if sheet['a'] == detail['a'] and sheet['b'] == detail['b']:
        sheet['det'] = details.index(detail)
        detail['sum'] -= 1
        if not main():
            if detail['a'] < detail['b']:
                detail['a'], detail['b'] = detail['b'], detail['a']
            detail['sum'] += 1
            return False
    return True


def cut_horizontal(sheet, detail):
    global rubber_square
    if sheet['b'] == detail['b']:
        return False
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
    if not main():
        # for x in range(2):
        res.pop()
        last_record = res.pop()
        if last_record['det'] == 'n':
            rubber_square -= last_record['a'] * last_record['b']
        return False
    return True


def cut_vertical(sheet, detail):
    global rubber_square
    if sheet['a'] == detail['a']:
        return False
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
    if not main():
        # for x in range(2):
        res.pop()
        last_record = res.pop()
        if last_record['det'] == 'n':
            rubber_square -= last_record['a'] * last_record['b']
        return False
    return True

get_details()
available_rubber_square = main_sheet['a'] * main_sheet['b'] - details_square
main()
for i in res:
    print(i)
