import os
import re

from constants import engine_infobox_regex, engine_code_regex, translation_table, page_file_path


def get_car_name_from_file_name(name):
    name = re.sub('[0-9]*_', '', name)
    name = re.sub('-', ' ', name)
    return re.sub('.xml', '', name)


def get_engine_codes(file_path_name):
    # print('Getting engine codes...')

    with open(file_path_name, encoding='utf-8') as file:
        print('Getting engine codes for: ' + file.name)

        engine_code_messy = find_engine_code_inside_infobox(file)
        for original, new in translation_table.items():
            engine_code_messy = engine_code_messy.replace(original, new)

        engine_code_messy = re.sub('\{\{ubl|[\{\}\[\]]*', '', engine_code_messy)

        # get only engine code
        if engine_code_messy != '':
            engine_codes = re.compile(engine_code_regex).findall(engine_code_messy)

            return remove_duplicates(engine_codes)


def find_engine_code_inside_infobox(file):
    found_engine = False
    engine_part = ''
    open_curly_brackets = 0
    for line in file:
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


def remove_duplicates(engine_codes):
    res = []

    for i in engine_codes:
        if i not in res:
            res.append(i)

    return res


def create_cars_index():
    car_index = {}

    index = 0
    for file_name in os.listdir(page_file_path):
        print(index)
        index += 1
        engine_codes = get_engine_codes(page_file_path + file_name)
        if engine_codes is not None:
            car_index[get_car_name_from_file_name(file_name)] = engine_codes

    return car_index


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