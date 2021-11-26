import re

from constants import engine_infobox_regex, engine_code_regex, translation_table, page_file_path


def get_car_name_from_file_name(name):
    name = re.sub('[0-9]*_', '', name)
    name = re.sub('-', ' ', name)
    return re.sub('.xml', '', name)


def find_engine_code_inside_infobox(lines):
    found_engine = False
    engine_part = ''
    open_curly_brackets = 0
    for line in lines:
        if re.search(engine_infobox_regex, line, re.IGNORECASE):
            found_engine = True

        if found_engine:
            if re.search('\{|\}', line):
                open_curly_brackets += line.count('{')
                open_curly_brackets -= line.count('}')

            if re.search(engine_code_regex, line):
                engine_part += line + '\n'

        if open_curly_brackets <= 0:
            found_engine = False


    # print(engine_part + '\n\n')
    return engine_part


def get_engine_codes(title, lines):
    # print('Getting engine codes...')

    print('Getting engine codes for: ' + title)

    engine_code_messy = find_engine_code_inside_infobox(lines)
    for original, new in translation_table.items():
        engine_code_messy = engine_code_messy.replace(original, new)

    engine_code_messy = re.sub('\{\{ubl|[\{\}\[\]]*', '', engine_code_messy)

    # get only engine code
    if engine_code_messy != '':
        engine_codes = re.compile(engine_code_regex).findall(engine_code_messy)

        return remove_duplicates(engine_codes)


def remove_duplicates(engine_codes):
    res = []

    for i in engine_codes:
        if i not in res:
            res.append(i)

    return res


def create_cars_index(title, text):
    new_indexes = []

    engine_codes = get_engine_codes(title, text.split('\n'))

    new_indexes.append([title, engine_codes])

    if engine_codes is not None:
        for engine_code in engine_codes:
            if engine_code is not None:
                new_indexes.append([engine_code, title])

    return new_indexes


def create_engine_index(car_index):
    engine_index = {}
    for car, engines_list in car_index.items():
        for engine in engines_list:
            engine_index[engine] = []
            engine_index[engine].append(car)

            for different_car, different_car_engines_list in car_index.items():
                if car == different_car:
                    continue
                if any(engine == different_car_engine for different_car_engine in different_car_engines_list):
                    engine_index[engine].append(different_car)

    print(engine_index)
    return engine_index