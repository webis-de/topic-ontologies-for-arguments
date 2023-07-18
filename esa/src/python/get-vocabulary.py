# coding=utf-8

import argparse
import csv
import collections
import math
import sys
csv.field_size_limit(sys.maxsize)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-file", dest="input_file", default=None, type=str, required=True, help="A CSV file that contains the texts from which the inverse document frequency should be calculated.")
    parser.add_argument("--text-columns", dest="text_columns", default="text", type=str, required=False, help="The column name(s), comma-separated, of the columns that contain the text. Each entry in each of these columns is treated as an own 'document'. Default: 'text'.")
    parser.add_argument("--base", dest="base", default=2, type=int, required=False, help="The logarithm base that is used to compute the inverse document frequency. Default is 2.")
    parser.add_argument("--output-file", dest="output_file", default=None, type=str, required=True, help="The output will be written to this file in CSV format with columns 'index', 'token', 'df', and 'idf'.")
    return parser.parse_args()

def get_unique_tokens(text):
    tokens = text.split(" ")
    unique_tokens = set(tokens)
    return unique_tokens

def calculate_idf(document_frequency, num_documents, base):
    nd = float(num_documents)
    df = float(document_frequency)
    return math.log(nd / df, base)

args = parse_args()
base = args.base

counter = collections.Counter()
num_documents = 0
with open(args.input_file, 'r') as input_file:
    reader = csv.DictReader(input_file)
    input_column_names = reader.fieldnames
    text_column_names = [name for name in input_column_names if name in args.text_columns.split(",")]
    for row in reader:
        for text_column_name in text_column_names:
            unique_tokens = get_unique_tokens(row[text_column_name])
            counter.update(unique_tokens)
            num_documents += 1

counts = counter.most_common()
tokens = [token for (token, document_frequency) in counts]
dfs = [document_frequency for (token, document_frequency) in counts]
idfs = [calculate_idf(document_frequency, num_documents, base) for document_frequency in dfs]
with open(args.output_file, 'w', newline='') as output_file:
    output_column_names = ['index','token','df','idf']
    writer = csv.writer(output_file, lineterminator="\n")
    writer.writerow(output_column_names) # header
    for t in range(len(tokens)):
        writer.writerow([t, tokens[t], dfs[t], idfs[t]])

