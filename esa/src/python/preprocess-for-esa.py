# coding=utf-8

import argparse
import csv
import re
import sys
csv.field_size_limit(sys.maxsize)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-file", dest="input_file", default=None, type=str, required=True, help="A CSV file that contains the text to be processed.")
    parser.add_argument("--text-columns", dest="text_columns", default="text", type=str, required=False, help="The column name(s), comma-separated, of the columns that contain the text to be processed. Default: 'text'.")
    parser.add_argument("--kept-columns", dest="kept_columns", default=None, type=str, required=False, help="The column name(s), comma-separated, of the columns that should be kept for the output. Default is to keep all.")
    parser.add_argument("--no-lemmatization", dest="lemmatize", action="store_false", help="Do not lemmatize the text.")
    parser.add_argument("--min-token-length", dest="min_token_length", default=4, type=int, required=False, help="The minimum number of characters a token must have (after lemmatization) so that it is not removed. Default is 4.")
    parser.add_argument("--output-file", dest="output_file", default=None, type=str, required=True, help="The output will be written to this file in CSV format and have the columns specified through --kept_columns and an additional column for each column in --text_columns where '-preprocessed' is added to the column name.")
    return parser.parse_args()

def get_lemmatizer(args):
    if args.lemmatize:
        import nltk
        nltk.download('wordnet')
        return nltk.stem.WordNetLemmatizer()
    else:
        return None

def get_min_token_length(args):
    return args.min_token_length

def get_output_column_names(args, input_column_names, text_column_names):
    preprocessed_column_names = [name + "-preprocessed" for name in text_column_names]
    if args.kept_columns == None:
        return input_column_names + preprocessed_column_names
    else:
        return [name for name in input_column_names if name in args.kept_columns.split(",")] + preprocessed_column_names

def preprocess_token(token, lemmatizer, min_token_length):
    if lemmatizer != None:
        token = lemmatizer.lemmatize(token.strip())
    if len(token) < min_token_length:
        return None
    else:
        return token

def preprocess_text(text, lemmatizer, min_token_length):
    text = text.lower()
    text = text.replace("\n", " ").replace("\r", " ")
    text = re.sub(r"https?://(?:[-\w.]|(?:%[\da-f]{2}))+", " ", text)
    text = re.sub("[^a-z]+", " ", text).replace("\s+", " ")
    tokens = [preprocess_token(token, lemmatizer, min_token_length) for token in text.split(" ")]
    tokens = [token for token in tokens if token != None]
    return " ".join(tokens)


args = parse_args()
lemmatizer = get_lemmatizer(args)
min_token_length = get_min_token_length(args)
with open(args.input_file, 'r') as input_file:
    reader = csv.DictReader(input_file)
    input_column_names = reader.fieldnames
    text_column_names = [name for name in input_column_names if name in args.text_columns.split(",")]
    with open(args.output_file, 'w', newline='') as output_file:
        output_column_names = get_output_column_names(args, input_column_names, text_column_names)
        writer = csv.DictWriter(output_file, output_column_names, lineterminator="\n", extrasaction='ignore') # extrasaction is used to ignore other columns
        writer.writeheader()
        for row in reader:
            for text_column_name in text_column_names:
                row[text_column_name + "-preprocessed"] = preprocess_text(row[text_column_name], lemmatizer, min_token_length)
            writer.writerow(row)

