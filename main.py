import re
import os


def extract_pages(wiki, output_file):
    inside_page = False
    found_title = False
    page = ''
    title = ''
    for line in wiki:
        if re.search('<page>', line, re.IGNORECASE):
            inside_page = True
            page = line
        if re.search('<title>', line, re.IGNORECASE) and re.search('Nissan', line, re.IGNORECASE):
            found_title = True
            output_file.write(page)
            output_file.write(line)
            title = re.sub('( *)?<[/]?title>(\n)?', '', line)
            print('Found title:' + title)
        if inside_page and found_title:
            output_file.write(line)
        if re.search('</page>', line, re.IGNORECASE):
            found_title = False
            inside_page = False


result_file_path = 'results.xml'

os.remove(result_file_path)
print('starting')
with open('data_sample/enwiki-latest-pages-articles1.xml-p1p41242', encoding='utf-8') as wiki:
    with open(result_file_path, 'a', encoding='utf-8') as output_file:
        extract_pages(wiki, output_file)
