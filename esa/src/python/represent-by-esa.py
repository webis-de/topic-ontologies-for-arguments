# coding=utf-8

import argparse
import csv
import pandas
import collections
import sys
csv.field_size_limit(sys.maxsize)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-file", dest="input_file", default=None, type=str, required=True, help="A CSV file that contains the texts to represent.")
    parser.add_argument("--id-column", dest="id_column", default="document.id", type=str, required=False, help="The column name of the column in the input file that contains the identifier for the text in the respective row. Default: 'document.id'.")
    parser.add_argument("--text-column", dest="text_column", default="text", type=str, required=False, help="The column name of the column in the input file that contains the text. Default: 'text'.")
    parser.add_argument("--vocabulary-file", dest="vocabulary_file", default=None, type=str, required=True, help="A CSV file that contains the tokens that correspond to each output dimension of the ESA.")
    parser.add_argument("--index-column", dest="index_column", default="index", type=str, required=False, help="The column name of the column in the vocabulary file that contains the index of the token in the representation. Default: 'index'.")
    parser.add_argument("--token-column", dest="token_column", default="token", type=str, required=False, help="The column name of the column in the vocabulary file that contains the token. Default: 'token'.")
    parser.add_argument("--idf-column", dest="idf_column", default="idf", type=str, required=False, help="The column name of the column in the vocabulary file that contains the inverse document frequencies of the respective token. Default: 'idf'.")
    parser.add_argument("--output-file", dest="output_file", default=None, type=str, required=True, help="The output will be written to this file in CSV format with columns '<value of --id-column>' and 'sparse-representation', where the sparse-representation is a dictionary from token-number (using the order from the vocabulary-file, starting by 0) to the corresponding TF*IDF value.")
    return parser.parse_args()

def get_documents(args):
    document_frame = pandas.read_csv(args.input_file, dtype=str)
    return (document_frame[args.id_column].values, document_frame[args.text_column].values)

def get_vocabulary(args):
    vocabulary_frame = pandas.read_csv(args.vocabulary_file, dtype={args.token_column:str,args.idf_column:float})
    tokens = vocabulary_frame[args.token_column].values
    indices = vocabulary_frame[args.index_column].values
    token_indices = dict(zip(tokens, indices))
    idfs = vocabulary_frame[args.idf_column].values
    return (token_indices, idfs)

def represent(document_text, token_indices, idfs):
    document_token_counter = collections.Counter(document_text.split(" "))
    document_tokens = [token for token in document_token_counter.keys() if token in token_indices]
    vocabulary_indices = [token_indices[token] for token in document_tokens]
    tfidfs = [document_token_counter[token] * idfs[token_indices[token]] for token in document_tokens]
    return dict(zip(vocabulary_indices, tfidfs))


args = parse_args()
document_id_column = args.id_column
document_text_column = args.text_column
(token_indices, idfs) = get_vocabulary(args)

with open(args.input_file, 'r') as input_file:
    document_reader = csv.DictReader(input_file)
    with open(args.output_file, 'w', newline='') as output_file:
        output_column_names = [document_id_column,'sparse-representation']
        writer = csv.writer(output_file, lineterminator="\n")
        writer.writerow(output_column_names) # header
        for document_row in document_reader:
            representation = represent(document_row[document_text_column], token_indices, idfs)
            writer.writerow([document_row[document_id_column], representation])

