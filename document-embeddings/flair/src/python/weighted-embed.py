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
import pandas
import io
import math
import re

flair.cache_root = 'flaircache'

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-file", dest="input_file", default=None, type=str, required=True, help="A CSV file that contains the texts to embed.")
    parser.add_argument("--id-column", dest="id_column", default="document.id", type=str, required=False, help="The name of the column that contains the identifier for the text in the respective row. Default: 'document.id'.")
    parser.add_argument("--text-column", dest="text_column", default="text", type=str, required=False, help="The name of the columns that contains the text. Default: 'text'.")
    parser.add_argument("--weights-file", dest="weights_file", default=None, type=str, required=True, help="A CSV file that contains the weights for each lemma.")
    parser.add_argument("--lemma-column", dest="lemma_column", default="token", type=str, required=False, help="The name of the column that contains the lemma in the --weights-file. Default: 'token'.")
    parser.add_argument("--weight-column", dest="weight_column", default="idf", type=str, required=False, help="The name of the columns that contains the weight for the lemma in the --weights-file. Default: 'idf'.")
    parser.add_argument("--out-of-vocabulary-weight", dest="out_of_vocabulary_weight", default=float('nan'), type=float, required=False, help="The weight to use if a token's lemma is not contained in the --weights-file. Default: The highest weight in the --weights-file.")
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
        raise Exception("Unknown embedding type: {}".format(args.embedding_type))

def create_embedder(args):
    print("Creating embedder")
    word_embedder = create_word_embedder(args)
    embedder = flair.embeddings.DocumentPoolEmbeddings([word_embedder], fine_tune_mode='none')
    print("Finished creating embedder")
    return embedder

def create_lemmatizer(args):
    import nltk
    nltk.download('wordnet', download_dir='./myvenv/lib/nltk_data')
    return nltk.stem.WordNetLemmatizer()

def preprocess_token(token):
    token = token.lower()
    token = re.sub(r"https?://(?:[-\w.]|(?:%[\da-f]{2}))+", "", token)
    token = re.sub("[^a-z]+", "", token)
    return token

def create_weighting_function(args):
    frame = pandas.read_csv(args.weights_file, dtype={args.lemma_column:str,args.weight_column:float})
    lemmas = frame[args.lemma_column].values
    weights = frame[args.weight_column].values
    weights_map = dict(zip(lemmas, weights))
    out_of_vocabulary_weight = args.out_of_vocabulary_weight
    if math.isnan(out_of_vocabulary_weight):
        out_of_vocabulary_weight = max(weights)
    lemmatizer = create_lemmatizer(args)
    def get_weight(token):
        token = preprocess_token(token)
        if token == "":
            return 0
        else:
            lemma = lemmatizer.lemmatize(token)
            if lemma in weights_map:
                return weights_map[lemma]
            else:
                return out_of_vocabulary_weight
    return get_weight

def embed_sentence(sentence, embedder, weighting_function, max_sentence_length):
    sentence_object = flair.embeddings.Sentence(sentence, use_tokenizer=True)
    if len(sentence_object) > max_sentence_length:
        print("Cutting sentence of %d tokens down to %d\n" % (len(sentence_object), max_sentence_length))
        tokens = [token.text for token in sentence_object[0:max_sentence_length]]
        cut_sentence = " ".join(tokens)
        sentence_object = flair.embeddings.Sentence(cut_sentence)
    if len(sentence_object) > 0:
        try:
            embedder.embed(sentence_object)
            embeddings = numpy.array([(token.embedding * weighting_function(token.text)).tolist() for token in sentence_object])
            return embeddings.mean(axis=0).tolist()
        except RuntimeError as err:
          print("Ignoring sentence of length %d\n" % (len(sentence_object)))
          print("Due to {0}".format(err))
          return None
    else:
        return None

def embed(text, embedder, weighting_function, max_sentence_length, max_sentences):
    sentences = segtok.segmenter.split_single(text)
    if len(sentences) > max_sentences:
        print("Sampling %d sentences down to %d\n" % (len(sentences), max_sentences))
        sentences = random.sample(sentences, k = max_sentences)
    embeddings = [embed_sentence(sentence, embedder, weighting_function, max_sentence_length) for sentence in sentences]
    embeddings = numpy.array([embedding for embedding in embeddings if embedding != None])
    embedding = embeddings.mean(axis=0).tolist()
    return embedding

args = parse_args()
embedder = create_embedder(args)
weighting_function = create_weighting_function(args)

with io.open(args.input_file, 'r', encoding="utf8") as input_file:
    document_reader = csv.DictReader(input_file)
    with open(args.output_file, 'w', newline='') as output_file:
        output_column_names = [args.id_column,'representation']
        writer = csv.writer(output_file, lineterminator="\n")
        writer.writerow(output_column_names) # header
        output_file.flush()
        for document_row in document_reader:
            representation = embed(document_row[args.text_column], embedder, weighting_function, args.max_sentence_length, args.max_sentences)
            writer.writerow([document_row[args.id_column], representation])
            output_file.flush()

