import lucene

from java.nio.file import Paths
from constants import index_path
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.analysis.standard import StandardAnalyzer

car = 'car'
engines = 'engines'
content = 'content'

lucene.initVM(vmargs=['-Djava.awt.headless=true'])

print('lucene', lucene.VERSION)

directory = SimpleFSDirectory(Paths.get(index_path))
searcher = IndexSearcher(DirectoryReader.open(directory))
analyzer = StandardAnalyzer()

command = ''
while command != 'exit':

    search_by = ''
    while (search_by != car and search_by != engines and search_by != content):
        selection = ''
        selection = input("Search by (1 - car; 2 - engine; Press enter to keep default('content')): ")
        if selection == '1':
            search_by = car
        elif selection == '2':
            search_by = engines
        elif selection == '':
            search_by = content

    command = input("Search term (to exit -> 'exit'): ")

    query = QueryParser(search_by, analyzer).parse("search " + command)
    scoreDocs = searcher.search(query, 50).scoreDocs

    print("%s total matching documents." % len(scoreDocs), '\n')

    for scoreDoc in scoreDocs:
        doc = searcher.doc(scoreDoc.doc)
        print(doc.get(car) + ': \n', doc.get(engines), '\n')