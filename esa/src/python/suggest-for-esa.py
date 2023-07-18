# coding=utf-8

import argparse
import csv
import ast
import scipy.sparse
import math
import sys
csv.field_size_limit(sys.maxsize)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--documents-file", dest="documents_file", default=None, type=str, required=True, help="A CSV file that contains at least the following columns: 'document.id' and 'sparse-representation', which contains the representation as a dictionary from index (token) to value (TF*IDF).")
    parser.add_argument("--topics-file", dest="topics_file", default=None, type=str, required=True, help="A CSV file that contains at least the following columns: 'topic.id' and 'sparse-representation', which contains the representation as a dictionary from index (token) to value (TF*IDF).")
    parser.add_argument("--vocabulary-size", dest="vocabulary_size", default=None, type=int, required=True, help="The number of entries in the employed vocabulary, which is equal to the representation size.")
    parser.add_argument("--method", dest="method", default="esa", type=str, required=False, help="The method name that will be written to each output row.")
    parser.add_argument("--output-file", dest="output_file", default=None, type=str, required=True, help="The output will be written to this file in CSV format with the columns 'document.id', 'topic.id', 'method', and 'score'. The column 'method' will always contain the value of --method.")
    return parser.parse_args()

def read_sparse_matrix(representation_file, id_column, vocabulary_size):
    num_columns = vocabulary_size
    num_rows = 0
    ids = []
    values = []
    row_indices = []
    column_indices = []
    norms = []
    with open(representation_file, 'r') as input_file:
        reader = csv.DictReader(input_file)
        for row in reader:
            ids.append(row[id_column])
            representation = ast.literal_eval(row["sparse-representation"])
            squared_norm = 0
            for (index, value) in representation.items():
                values.append(value)
                row_indices.append(num_rows)
                column_indices.append(index)
                squared_norm += value * value
            norms.append(math.sqrt(squared_norm))
            num_rows += 1
    return (ids, scipy.sparse.csr_matrix((values, (row_indices, column_indices)), shape=(num_rows, num_columns)), norms)

def reduce_representation(representation, num_entries):
    entries = [entry for entry in representation.items()]
    values = numpy.array([value for (index, value) in entries])
    top_values = numpy.argsort(values)[-num_entries:]
    indices = numpy.array([index for (index, value) in entries])[top_values]
    values = values[top_values]
    return dict(zip(indices, values))


args = parse_args()
vocabulary_size = args.vocabulary_size
method = args.method

(document_ids, document_matrix, document_norms) = read_sparse_matrix(args.documents_file, 'document.id', vocabulary_size)
(topic_ids, topic_matrix, topic_norms) = read_sparse_matrix(args.topics_file, 'topic.id', vocabulary_size)

output_matrix = document_matrix * topic_matrix.transpose()

with open(args.output_file, 'w', newline='') as output_file:
    output_column_names = ['document.id', 'topic.id', 'method', 'score']
    writer = csv.DictWriter(output_file, output_column_names, lineterminator="\n")
    writer.writeheader()
    for d in range(len(document_ids)):
        document_id = document_ids[d]
        dot_products = output_matrix.data[output_matrix.indptr[d]:output_matrix.indptr[d+1]]
        topic_indices = output_matrix.indices[output_matrix.indptr[d]:output_matrix.indptr[d+1]]
        for t in range(len(topic_indices)):
            topic_index = topic_indices[t]
            score = dot_products[t] / (document_norms[d] * topic_norms[topic_index])
            topic_id = topic_ids[topic_index]
            writer.writerow({'document.id':document_id,'topic.id':topic_id,'method':method,'score':score})


