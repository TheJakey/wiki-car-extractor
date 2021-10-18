import json

from sklearn.feature_extraction.text import TfidfVectorizer
import regex as re
import os

from constants import car_makers, translation_table, page_file_path, page_file_type, engine_infobox_regex, \
    engine_code_regex, extract_pages

# TODO: Frekvencny slovnik na filtrovanie stranok, ktore niesu o aute (Ludia napr. - Francis Ford Coppola)
# TODO: TF-IDF by malo mat zmysel, skus to pridat do indexu (surovo ako kod_motora: 2JZ-GTE, tf-idf: 0.69)
def extract_pages_from_file(wiki):
    inside_page = False
    found_title = False
    page = ''
    title = ''
    file = None
    file_num = 0
    for line in wiki:
        if re.search('<page>', line, re.IGNORECASE):
            inside_page = True
            page = line
        if re.search('<title>', line, re.IGNORECASE) and any(maker + ' ' in line for maker in car_makers):
            found_title = True
            title = re.sub('( *)?<[/]?title>(\n)?', '', line)

            file = open(page_file_path + str(file_num) + '_' + title + page_file_type, 'a', encoding='utf-8')
            file_num += 1

            file.write(page)
            file.write(line)

            print('Found title:' + title)
        if inside_page and found_title:
            file.write(line)
        if re.search('</page>', line, re.IGNORECASE):
            if file is not None:
                file.close()

            file = None
            found_title = False
            inside_page = False


def find_whole_infobox(file):
    infobox = ''
    open_curly_brackets = 0
    for line in file:
        if re.search('Infobox automobile', line, re.IGNORECASE):
            open_curly_brackets += 2
        if open_curly_brackets > 0:
            infobox += line
        if open_curly_brackets > 0 and re.search('}}', line):
            open_curly_brackets -= 2

    print(infobox + '\n\n')
    return infobox


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
            print(engine_codes)
            print()
            return engine_codes


def remove_previous_results():
    for file in os.listdir(page_file_path):
        os.remove(page_file_path + file)


def get_car_name_from_file_name(name):
    name = re.sub('[0-9]*_', '', name)
    return re.sub('.xml', '', name)


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


def calculate_and_print_tf_idf(car_index):
    corpus = []
    for car, engines_list in car_index.items():
        document = ''
        for engine in engines_list:
            document += engine + ' '
        corpus.append(document)
    print(corpus)
    vectorizer = TfidfVectorizer()
    values = vectorizer.fit_transform(corpus)
    print('TF-IDF Values')
    print(json.dumps(dict(zip(vectorizer.get_feature_names(), values.toarray()[0])), indent=4, sort_keys=True))


def main():
    print('starting')

    if extract_pages:
        with open('data_sample/enwiki-latest-pages-articles1.xml-p1p41242', encoding='utf-8') as wiki:
            remove_previous_results()
            extract_pages_from_file(wiki)

    car_index = create_cars_index()
    engine_index = create_engine_index(car_index)

    command = ''
    while command != 'exit':
        command = input("Insert Brand and/or Model: ")
        if command in car_index:
            print(car_index[command])
        elif command in engine_index:
            print(engine_index[command])
        elif command == 'tfidf':
            calculate_and_print_tf_idf(car_index)


main()
