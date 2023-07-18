import argparse
import csv
import sys
import numpy
csv.field_size_limit(sys.maxsize)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--documents-file", dest="documents_file", default=None, type=str, required=True, help="A CSV file that contains at least the following columns: 'document.id' and 'representation', which contains the representation as a list of floats.")
    parser.add_argument("--topics-file", dest="topics_file", default=None, type=str, required=True, help="A CSV file that contains at least the following columns: 'topic.id' and 'representation', which contains the representation as a list of floats..")
    parser.add_argument("--method", dest="method", default=None, type=str, required=True, help="The method name that will be written to each output row.")
    parser.add_argument("--output-file", dest="output_file", default=None, type=str, required=True, help="The output will be written to this file in CSV format with the columns 'document.id', 'topic.id', 'method', and 'score'. The column 'method' will always contain the value of --method.")
    return parser.parse_args()

def parse_representation(representation_string):
    return numpy.fromstring(representation_string.strip("[]"), dtype=float, sep=",")

def read_representation(filename, id_column):
    with open(filename, "r") as representation_file:
        reader = csv.DictReader(representation_file)
        ids = []
        representations = []
        for row in reader:
            representation = parse_representation(row["representation"])
            if len(representation) != 1:
                ids.append(row[id_column])
                representations.append(representation)
        return ids, representations

args = parse_args()
document_ids, document_representations = read_representation(args.documents_file, "document.id")
topic_ids, topic_representations = read_representation(args.topics_file, "topic.id")
method_name = args.method

document_norms = numpy.linalg.norm(document_representations, axis=1)
topic_norms = numpy.linalg.norm(topic_representations, axis=1)
scores = numpy.matmul(document_representations, numpy.transpose(topic_representations))

with open(args.output_file, 'w', newline='') as output_file:
    output_column_names = ['document.id', 'topic.id', 'method', 'score']
    writer = csv.DictWriter(output_file, output_column_names, lineterminator="\n")
    writer.writeheader()
    for d in range(len(scores)):
        for t in range(len(scores[d])):
            norm = (document_norms[d] * topic_norms[t])
            score = 0
            if norm != 0:
                score = scores[d][t] / norm
            writer.writerow({'document.id':document_ids[d],'topic.id':topic_ids[t],'method':method_name,'score':score})

