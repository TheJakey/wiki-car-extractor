wiki_article_pages_xml_filename = 'enwiki-latest-pages-articles.xml'
export_directoryname = 'cars-giant-export'

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

index_path = 'index'
processed_data_path = 'parsed_car_data/cars-giant-export/'