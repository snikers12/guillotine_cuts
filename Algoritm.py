from Shape import Shape
import Cut

sheet = {
    'x': 0,
    'y': 0,
    'a': 52,
    'b': 25,
    'ref_id': None,
    'cut': None,
    'det': 'l',
    'm': None
}

res = list(sheet)
details = list()

def get_details():
    f = open('details.txt', 'r')
    for line in f:
        s = line.split()
        details.append({
            'a': s[0],
            'b': s[1]
        })

def main():
    pass

def get_sheet(act_list):
    sheets_list = [item for item in act_list if item['det'] == 'l' and item['cut'] is None]
    if sheets_list:
        return sheets_list[-1]
    else:
        return False

def get_detail(details_list):
    if details_list:
        return details[0]
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
    if sheet['b'] <= detail['b']:
        return False
    sheet['cut'] = 0
    sheet['m'] = detail['b']
    main()

def cut_vertical(sheet, detail):
    if sheet['a'] <= detail['a']:
        return False
    sheet['cut'] = 0
    sheet['m'] = detail['a']
    main()

get_details()


