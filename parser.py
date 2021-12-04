import regex as re
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

from pages_indexer import create_cars_index
from constants import car_makers, engine_infobox_regex, engine_code_regex, translation_table


# TODO: Frekvencny slovnik na filtrovanie stranok, ktore niesu o aute (Ludia napr. - Francis Ford Coppola)


def remove_duplicates(engine_codes):
    res = []

    for i in engine_codes:
        if i not in res:
            res.append(i)

    return res


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


def create_cars_index(title, text):
    new_indexes = []

    engine_codes = get_engine_codes(title, text.split('\n'))

    new_indexes.append([title, engine_codes])

    if engine_codes is not None:
        for engine_code in engine_codes:
            if engine_code is not None:
                new_indexes.append([engine_code, title])

    return new_indexes


session = SparkSession.builder.getOrCreate()
session.sparkContext.setLogLevel('WARN')

dataframe = session.read.format('xml').options(rowTag='page').load('enwiki-latest-pages-articles1.xml')

dataframe.select("title", col("revision.text._VALUE").alias('text')) \
    .dropna(how='any') \
    .rdd \
    .filter(lambda page: any(maker + ' ' in page['title'] for maker in car_makers)) \
    .flatMap(lambda page: create_cars_index(page['title'], page['text'])) \
    .filter(lambda index: index[1] is not None) \
    .groupByKey() \
    .mapValues(list) \
    .saveAsTextFile('cars-index-final-export')
