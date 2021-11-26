import json

import regex as re
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from sklearn.feature_extraction.text import TfidfVectorizer

from constants import extract_pages_enabled, car_makers
from pages_indexer import create_cars_index, create_engine_index

# TODO: Frekvencny slovnik na filtrovanie stranok, ktore niesu o aute (Ludia napr. - Francis Ford Coppola)
# TODO: TF-IDF by malo mat zmysel, skus to pridat do indexu (surovo ako kod_motora: 2JZ-GTE, tf-idf: 0.69)


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


def export_indexes_to_file():
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


def main():
    print('starting')

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

if (extract_pages_enabled):
    export_indexes_to_file()
else:
    main()
