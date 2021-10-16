import re
import os

from constants import car_makers

engine_code_regex = '[\w-]{0,}([a-zA-Z-]{1,}[0-9]|[0-9][a-zA-Z-]{1,})[\w-]{0,}'
page_file_path = 'results/'

page_file_type = '.xml'

extract_pages = False

# fo = open("foo.txt", "wb")
# print "Name of the file: ", fo.name
# # Close opend file
# fo.close()
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
    engine_part = ''
    open_curly_brackets = 0
    for line in file:
        if re.search('\|[ \t]*engine[ \t]*=[ \t]*\{\{', line, re.IGNORECASE):
            open_curly_brackets = 2
        elif open_curly_brackets > 0 and re.search('\{\{', line):
                open_curly_brackets += 2
        if open_curly_brackets > 0 and re.search(engine_code_regex, line):
            engine_part += line

        if open_curly_brackets > 0 and re.search('\}\}', line):
            open_curly_brackets -= 2

    print(engine_part + '\n\n')
    return engine_part


def get_engine_codes(file_path_name):
    print('Getting engine codes...')

    with open(file_path_name, encoding='utf-8') as file:
        # find_whole_infobox(file)
        find_engine_code_inside_infobox(file)


def remove_previous_results():
    for file in os.listdir(page_file_path):
        os.remove(page_file_path + file)


def main():
    result_file_path = 'results.xml'

    # os.remove(result_file_path)
    print('starting')

    if extract_pages:
        with open('data_sample/enwiki-latest-pages-articles1.xml-p1p41242', encoding='utf-8') as wiki:
            remove_previous_results()
            extract_pages_from_file(wiki)

    index = 0
    for file_name in os.listdir(page_file_path):
        print(index)
        index += 1
        get_engine_codes(page_file_path + file_name)


main()
