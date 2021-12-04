import os
import ast
import lucene
from java.nio.file import Paths
from constants import index_path
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import IndexWriter, IndexWriterConfig
from org.apache.lucene.document import Document, Field, TextField
from org.apache.lucene.store import SimpleFSDirectory

from constants import processed_data_path


def create_document(key, value, writer):
    if (key is None or value is None):
        return

    doc = Document()
    doc.add(Field("key", key, TextField.TYPE_STORED))
    doc.add(Field("value", str(value), TextField.TYPE_STORED))
    writer.addDocument(doc)


def create_documents():
    for line in file.readlines():
        # dummy verification that read line contains expected data
        if line is not None and not line.startswith('('):
            continue

        line_formatted = ast.literal_eval(line)

        create_document(line_formatted[0], line_formatted[1], writer)


lucene.initVM(vmargs=['-Djava.awt.headless=true'])

store = SimpleFSDirectory(Paths.get(index_path))
analyzer = StandardAnalyzer()
config = IndexWriterConfig(analyzer)
config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
writer = IndexWriter(store, config)

for file_name in os.listdir(processed_data_path):
    with open(processed_data_path + file_name, encoding='utf-8') as file:
        create_documents()

# This may be a costly operation, so you should test the cost
# in your application and do it only when really necessary.
writer.commit()
writer.close()