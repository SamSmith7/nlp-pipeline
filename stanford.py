import os
java_path = r'/usr/lib/jvm/java-8-openjdk/bin/java'
os.environ['JAVAHOME'] = java_path

from nltk.parse.stanford import StanfordParser


scp = StanfordParser(
    path_to_jar='../stanford-parser/stanford-parser.jar',
    path_to_models_jar='../stanford-parser/stanford-parser-3.5.2-models.jar'
)

def parse(docs):

    parsed_docs = []

    for doc in docs:

        parsed_docs.append(list(scp.raw_parse(doc)))

    return parsed_docs
