# coding=utf-8

import argparse
import flair.embeddings
import flair
import torch
import segtok.segmenter
import numpy
import random
import csv
import sys
csv.field_size_limit(sys.maxsize)
import io

flair.cache_root = 'flaircache'

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-file", dest="input_file", default=None, type=str, required=True, help="A CSV file that contains the texts to embed.")
    parser.add_argument("--id-column", dest="id_column", default="document.id", type=str, required=False, help="The name of the column that contains the identifier for the text in the respective row. Default: 'document.id'.")
    parser.add_argument("--text-column", dest="text_column", default="text", type=str, required=False, help="The name of the columns that contains the text. Default: 'text'.")
    parser.add_argument("--embedding-type", dest="embedding_type", default="elmo", type=str, required=False, help="The word embedding method. One of 'bert', 'elmo', 'flair', or 'glove'. Default: 'elmo'.")
    parser.add_argument("--max-sentences", dest="max_sentences", default=10000, type=int, required=False, help="The maximum number of sentences to be used for each document. Sentences are sampled at random for documents with more sentences. Default: 10000.")
    parser.add_argument("--max-sentence-length", dest="max_sentence_length", default=200, type=int, required=False, help="The maximum number of tokens in sentences. Sentences with more tokens are truncated. Default: 200.")
    parser.add_argument("--output-file", dest="output_file", default=None, type=str, required=True, help="The output will be written to this file in CSV format with columns '<value of --id-column>' and 'representation', where the representation is the dense embedding vector as list.")
    return parser.parse_args()

def create_word_embedder(args):
    if args.embedding_type == "bert":
        return flair.embeddings.BertEmbeddings()
    elif args.embedding_type == "elmo":
        return flair.embeddings.ELMoEmbeddings()
    elif args.embedding_type == "flair":
        return flair.embeddings.FlairEmbeddings('news-forward-fast')
    elif args.embedding_type == "glove":
        return flair.embeddings.WordEmbeddings('glove')
    else:
        raise Exception("Unknown embedding type: {}".foramt(args.embedding_type))

def create_embedder(args):
    print("Creating embedder")
    word_embedder = create_word_embedder(args)
    embedder = flair.embeddings.DocumentPoolEmbeddings([word_embedder], fine_tune_mode='none')
    print("Finished creating embedder")
    return embedder

def embed_sentence(embedder, sentence, max_sentence_length):
    sentence_object = flair.embeddings.Sentence(sentence, use_tokenizer=True)
    if len(sentence_object) > max_sentence_length:
        print("Cutting sentence of %d tokens down to %d\n" % (len(sentence_object), max_sentence_length))
        tokens = [token.text for token in sentence_object[0:max_sentence_length]]
        cut_sentence = " ".join(tokens)
        sentence_object = flair.embeddings.Sentence(cut_sentence)
    if len(sentence_object) > 0:
        try:
            embedder.embed(sentence_object)
            return sentence_object.get_embedding().tolist()
        except RuntimeError as err:
          print("Ignoring sentence of length %d\n" % (len(sentence_object)))
          print("Due to {0}".format(err))
          return None
    else:
        return None

def embed(embedder, text, max_sentence_length, max_sentences):
    sentences = segtok.segmenter.split_single(text)
    if len(sentences) > max_sentences:
        print("Sampling %d sentences down to %d\n" % (len(sentences), max_sentences))
        sentences = random.sample(sentences, k = max_sentences)
    embeddings = [embed_sentence(embedder, sentence, max_sentence_length) for sentence in sentences]
    embeddings = numpy.array([embedding for embedding in embeddings if embedding != None])
    embedding = embeddings.mean(axis=0).tolist()
    return embedding

args = parse_args()
embedder = create_embedder(args)

with io.open(args.input_file, 'r', encoding="utf8") as input_file:
    document_reader = csv.DictReader(input_file)
    with open(args.output_file, 'w', newline='') as output_file:
        output_column_names = [args.id_column,'representation']
        writer = csv.writer(output_file, lineterminator="\n")
        writer.writerow(output_column_names) # header
        output_file.flush()
        for document_row in document_reader:
            representation = embed(embedder, document_row[args.text_column], args.max_sentence_length, args.max_sentences)
            writer.writerow([document_row[args.id_column], representation])
            output_file.flush()

