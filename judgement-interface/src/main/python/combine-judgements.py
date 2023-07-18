# coding=utf-8

import argparse
import csv
import sys
import operator
import math
csv.field_size_limit(sys.maxsize)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--judgements-file", dest="judgements_file", default=None, type=str, required=True, help="A CSV file that contains at least the following columns: 'document.id' and 'topic.id'")
    parser.add_argument("--suggestions-file", dest="suggestions_file", default=None, type=str, required=True, help="A CSV file that contains at least the following columns: 'document.id', 'topic.id', 'method', and 'score'.")
    parser.add_argument("--output-file", dest="output_file", default=None, type=str, required=True, help="The output will be written to this file in CSV format.")
    return parser.parse_args()

SCORE_ZERO_RANK = 100000

def read_suggestions(args):
    with open(args.suggestions_file, 'r') as suggestions_file:
        scores = {}
        reader = csv.DictReader(suggestions_file)
        for row in reader:
            document_id = row["document.id"]
            topic_id = row["topic.id"]
            method = row["method"]
            score = row["score"]
            if method not in scores:
                scores[method] = {}
            if document_id not in scores[method]:
                scores[method][document_id] = {}
                scores[method][document_id]["scores"] = {}
                scores[method][document_id]["ranks"] = {}
            scores[method][document_id]["scores"][topic_id] = float(score)
        for method in scores:
            for document_id in scores[method]:
                for ontology in range(1, 6):
                    ontology_scores = filter(lambda x: math.floor(float(x[0])) == ontology, scores[method][document_id]["scores"].items())
                    sorted_topics = sorted(ontology_scores, key=operator.itemgetter(1), reverse=True)
                    i = 0
                    rank = 0
                    last_score = float("inf")
                    for (topic_id, score) in sorted_topics:
                        i += 1
                        if score < last_score - 0.000000001:
                            rank = i
                        if score == 0:
                            rank = SCORE_ZERO_RANK
                        scores[method][document_id]["ranks"][topic_id] = rank
                        last_score = score
        return scores


args = parse_args()
scores = read_suggestions(args)
methods = scores.keys()

with open(args.judgements_file, 'r') as judgements_file:
    reader = csv.reader(judgements_file)
    input_column_names = next(reader)
    with open(args.output_file, 'w', newline='') as output_file:
        output_column_names = input_column_names
        for method in methods:
            output_column_names.append(method + ".score")
            output_column_names.append(method + ".rank")
        writer = csv.DictWriter(output_file, output_column_names, lineterminator="\n")
        writer.writeheader()
        for row in reader:
            output_row = dict(zip(input_column_names, row))
            document_id = output_row["document.id"]
            topic_id = output_row["topic.id"]
            for method in methods:
                score = 0
                rank = 0
                if document_id in scores[method]:
                    if topic_id in scores[method][document_id]["scores"]:
                        score = scores[method][document_id]["scores"][topic_id]
                        rank = scores[method][document_id]["ranks"][topic_id]
                    else:
                        ontology = math.floor(float(topic_id))
                        ontology_ranks = [r for (_, r) in filter(lambda x: math.floor(float(x[0])) == ontology, scores[method][document_id]["ranks"].items())]
                        max_rank = 0
                        if len(ontology_ranks) > 0:
                            max_rank = max(ontology_ranks)
                        rank = max_rank + 1
                output_row[method + ".score"] = score
                output_row[method + ".rank"] = rank
            writer.writerow(output_row)

