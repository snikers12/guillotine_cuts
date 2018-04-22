main_sheet = {
    'x': 0,
    'y': 0,
    'a': 52,
    'b': 25,
    'ref_id': None,
    'cut': None,
    'det': 'l',
    'm': None
}

main_sheet_square = main_sheet['a'] * main_sheet['b']
res = list(main_sheet)
details = list()
details_square = 0


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


def main(res_list, details_list):
    dets = details_list
    sheets = get_sheet(res_list)
    for sheet in sheets:
        result = False
        for detail in dets:
            if detail['sum'] == 0:
                continue
            if place_horizontal(sheet, detail) or place_vertical(sheet, detail):
                if cut_horizontal(sheet, detail) or cut_vertical(sheet, detail):
                    result = True
                    break
        if not result:
            sheet['det'] = 'n'


def get_sheet(act_list):
    return [item for item in act_list if item['det'] == 'l' and item['cut'] is None]


def get_detail(details_list):
    if details_list:
        detail = details_list.pop(0)
        return detail
    else:
        return False


def place_horizontal(sheet, detail):
    if sheet['a'] < detail['a'] or sheet['b'] < detail['b']:
        return False
    is_detail(sheet, detail)


def place_vertical(sheet, detail):
    if sheet['b'] < detail['a'] or sheet['a'] < detail['b']:
        return False
    detail['a'], detail['b'] = detail['b'], detail['a']
    is_detail(sheet, detail)


def is_detail(sheet, detail):
    if sheet['a'] == detail['a'] and sheet['b'] == detail['b']:
        sheet['det'] = details.index(detail)
        main()


def cut_horizontal(sheet, detail):
    sheet['cut'] = 0
    sheet['m'] = detail['b']
    main()


def cut_vertical(sheet, detail):
    sheet['cut'] = 0
    sheet['m'] = detail['a']
    main()


get_details()
