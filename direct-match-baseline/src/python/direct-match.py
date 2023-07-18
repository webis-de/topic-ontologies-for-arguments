# coding=utf-8

import argparse
import pandas
import re
import numpy
from suffix_trees import STree

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--documents-file", dest="documents_file", default=None, type=str, required=True, help="A CSV file with (at least) the columns 'document.id' and 'text'.")
    parser.add_argument("--topics-file", dest="topics_file", default=None, type=str, required=True, help="A CSV file with (at least) the columns 'topic.id' and 'name'.")
    parser.add_argument("--output-file", dest="output_file", default=None, type=str, required=True, help="The output will be written to this file in CSV format and have the columns 'document.id', 'topic.id', 'method', and 'score', where the 'method' column will always contains the string 'direct-match' and 'score' will contain 1 if the 'name' of the topic with the respective 'topic.id' occurs in the 'text' of the document with the respective 'document.id' and 0 otherwise.")
    return parser.parse_args()

def normalize_text(text):
    return re.sub(r'\s+', ' ', re.sub(r'[^a-z0-9 ]', '', text.lower()))


args = parse_args()
documents = pandas.read_csv(args.documents_file, dtype={"document.id":object,"text":object})
document_ids = documents['document.id'].values
document_texts = documents['text'].values
topics = pandas.read_csv(args.topics_file, dtype={"topic.id":object,"text":object})
topic_ids = topics['topic.id'].values
topic_names = topics['name'].values

output_document_ids = numpy.repeat(document_ids, len(topic_ids)).tolist()
output_topic_ids = numpy.repeat([topic_ids], len(document_ids), axis=0).flatten().tolist()
output_methods = numpy.repeat(["direct-match"], len(output_document_ids)).tolist()
output_scores = numpy.repeat(0, len(output_document_ids)).tolist()

idx = 0
for d in range(len(document_ids)):
    document_id = document_ids[d]
    document_text = normalize_text(document_texts[d])
    if document_text:
        comparison_tree = STree.STree(document_text)
        for t in range(len(topic_ids)):
            topic_id = topic_ids[t]
            topic_name = normalize_text(topic_names[t])
            if document_text.startswith(topic_name) or document_text.endswith(topic_name) or comparison_tree.find(" " + topic_name + " ") != -1:
                output_scores[idx] = 1
            idx += 1
    else:
        idx += len(topic_ids)


output = pandas.DataFrame({'document.id':output_document_ids,'topic.id':output_topic_ids,'method':output_methods,'score':output_scores}, columns = ['document.id','topic.id','method','score'])
output.to_csv(args.output_file, index=False)

