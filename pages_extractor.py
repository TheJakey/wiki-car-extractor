import os
import re

from constants import all_but_supported_chars_for_file_name, page_file_path, page_file_type, car_makers


def toFileName(potential_file_name):
    return re.sub(all_but_supported_chars_for_file_name, '-', potential_file_name)


def verify_if_page_contains_car(file):
    if file is None:
        return

    # file has to be closed before it can be read - because now it's opened in W mode
    file_name = file.name
    file.close()

    # open file in R mode to read and analyze it's content
    file = open(file_name, 'r', encoding='utf-8')

    engine_occurrence = 0
    for line in file.readlines():
        engine_occurrence += line.lower().split().count('engine')

    file.close()

    # 5 -> 79 files - 0 persons
    # 3 -> 116 files - 0 persons
    if engine_occurrence < 3:
        os.remove(file_name)


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

            file = open(page_file_path + str(file_num) + '_' + toFileName(title) + page_file_type, 'w',
                        encoding='utf-8')
            file_num += 1

            file.write(page)
            file.write(line)

            print('Found title:' + title)
        if inside_page and found_title:
            file.write(line)
        if re.search('</page>', line, re.IGNORECASE):
            if file is not None:
                verify_if_page_contains_car(file)

            file = None
            found_title = False
            inside_page = False


def remove_previous_results():
    for file in os.listdir(page_file_path):
        os.remove(page_file_path + file)


def extract_pages(wiki_pages_articles_location):
    with open(wiki_pages_articles_location, encoding='utf-8') as wiki:
        remove_previous_results()
        extract_pages_from_file(wiki)