extract_pages_enabled = True

car_makers = ['Acura',
              'Alfa Romeo',
              'Audi',
              'BMW',
              'Bentley',
              'Buick',
              'Cadillac',
              'Chevrolet',
              'Chrysler',
              'Dodge',
              'Fiat',
              'Ford',
              'GMC',
              'Genesis',
              'Honda',
              'Hyundai',
              'Infiniti',
              'Jaguar',
              'Jeep',
              'Kia',
              'Land Rover',
              'Lexus',
              'Lincoln',
              'Lotus',
              'Lucid',
              'Maserati',
              'Mazda',
              'Mercedes-Benz',
              'Mercury',
              'Mini',
              'Mitsubishi',
              'Nissan',
              'Polestar',
              'Pontiac',
              'Porsche',
              'Ram',
              'Rivian',
              'Rolls-Royce',
              'Saab',
              'Saturn',
              'Scion',
              'Smart',
              'Subaru',
              'Suzuki',
              'Tesla',
              'Toyota',
              'Volkswagen',
              'Volvo']

translation_table = {
    '&amp;nbsp;': ' ',
    ' |': '\n',
    '|': ' ',
    '\\': '',
    'engine =': '',
    'engine=': ''
}

engine_infobox_regex = '\|[ \t]*engine[ \t]*=[ \t]*\{\{'

engine_code_regex = '[a-zA-Z0-9_]*(?:[a-zA-Z]+[-/]*[0-9]|[-/]*[0-9][a-zA-Z]+)[a-zA-Z0-9_]*'

all_but_supported_chars_for_file_name = '[^a-zA-ZÀ-ž0-9]'

page_file_path = 'results/'

page_file_type = '.xml'
