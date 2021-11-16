import os
import re

from constants import all_but_supported_chars_for_file_name, page_file_path, page_file_type


def toFileName(potential_file_name):
    return re.sub(all_but_supported_chars_for_file_name, '-', potential_file_name)


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

            file = open(page_file_path + str(file_num) + '_' + toFileName(title) + page_file_type, 'a',
                        encoding='utf-8')
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


def remove_previous_results():
    for file in os.listdir(page_file_path):
        os.remove(page_file_path + file)


def extract_pages(wiki_pages_articles_location):
    with open(wiki_pages_articles_location, encoding='utf-8') as wiki:
        remove_previous_results()
        extract_pages_from_file(wiki)