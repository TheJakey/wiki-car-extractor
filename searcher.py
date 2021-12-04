import lucene

from java.nio.file import Paths
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.analysis.standard import StandardAnalyzer

lucene.initVM(vmargs=['-Djava.awt.headless=true'])

print('lucene', lucene.VERSION)

directory = SimpleFSDirectory(Paths.get("tempIndex"))
searcher = IndexSearcher(DirectoryReader.open(directory))
analyzer = StandardAnalyzer()

command = ''
while command != 'exit':
    command = input("Insert Brand and/or Model: ")

    query = QueryParser('value', analyzer).parse("search " + command)
    scoreDocs = searcher.search(query, 50).scoreDocs

    print("%s total matching documents." % len(scoreDocs))

    for scoreDoc in scoreDocs:
        doc = searcher.doc(scoreDoc.doc)
        print('result:', doc.get('key'))