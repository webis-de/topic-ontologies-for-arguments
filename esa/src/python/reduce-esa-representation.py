# coding=utf-8

import argparse
import csv
import ast
import numpy
import sys
csv.field_size_limit(sys.maxsize)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-file", dest="input_file", default=None, type=str, required=True, help="A CSV file that contains the representation as a dictionary from index to value.")
    parser.add_argument("--representation-column", dest="representation_column", default="sparse-representation", type=str, required=False, help="The column name of the column in the input file that contains the representation. Default: 'sparse-representation'.")
    parser.add_argument("--num-entries", dest="num_entries", default=1000, type=int, required=False, help="The maximum number of non-zero entries that each representation is allowed to have. For representations with more none-zero entries, the <--num-entries> entries with the highest values are kept. Default is 1000.")
    parser.add_argument("--output-file", dest="output_file", default=None, type=str, required=True, help="The output will be written to this file in the same format as the input file. Only the <--representation-column> fields will be modified.")
    return parser.parse_args()

def reduce_representation(representation, num_entries):
    entries = [entry for entry in representation.items()]
    values = numpy.array([value for (index, value) in entries])
    top_values = numpy.argsort(values)[-num_entries:]
    indices = numpy.array([index for (index, value) in entries])[top_values]
    values = values[top_values]
    return dict(zip(indices, values))


args = parse_args()
representation_column = args.representation_column
num_entries = args.num_entries

with open(args.input_file, 'r') as input_file:
    reader = csv.DictReader(input_file)
    with open(args.output_file, 'w', newline='') as output_file:
        writer = csv.DictWriter(output_file, reader.fieldnames, lineterminator="\n") # same header
        writer.writeheader()
        for row in reader:
            representation = ast.literal_eval(row[representation_column])
            row[representation_column] = "%s" % reduce_representation(representation, num_entries)
            writer.writerow(row)

