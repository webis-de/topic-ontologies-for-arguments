#!/usr/bin/env python3

import pickle
import argparse

from matrix import ESAMatrix
from preprocessor import Preprocessor


def create_arg_parser():
    parser = argparse.ArgumentParser(description = "Computes the ESA-matrix for the specified corpus.")
    parser.add_argument("-i", action = "store", required = True, \
                    help = "The path to the input corpus. The file to be processed should be a csv file\
                            separated by commas, containing two columns, 'concept' and 'text', the first\
                            should only contain the name of the concept, the second should contain all\
                            text of that concept. (It is ideal to create that file with pandas 'to_csv' method,\
                            otherwise it could be the case that there may be errors, with some unproperly escaped\
                            characters).")
    parser.add_argument("-o", action = "store", required = True, \
                    help = "The path to the location of the produced output file.")
    parser.add_argument("-l", action = "store_true", default = False, required = False, \
                    help = "If this flag is set, lemmatization is performed and words not present in the specified vocabulary \
                            are removed. If this flag is absent no lemmatization is performed and all words from the corpus are kept.")
    parser.add_argument("-v", action = "store", required = False, \
                    help = "The path to the vocabulary, only necessary if the '-l' flag is set. (../../../../resources/esa-w2v/w2v-vocab.p)")
    return parser


def main():
    parser = create_arg_parser()
    args = parser.parse_args()
    args = vars(args)
    print(args)
    corpus_path = args["i"]
    #"../../../../resources/corpora/" + "debatepedia" + ".csv"
    matrix_path = args["o"]
    #"../../../../resources/esa-w2v/" + "debatepedia" + ".mat"  

    lemma = args["l"]
    vocab_path = args["v"] 
    #"../../../../resources/esa-w2v/w2v-vocab.p"

    if lemma and vocab_path is None:
        parser.error("lemma requires vocab")

    print(f"Starting preprocessing ...")
    print(f"    Corpus: {corpus_path}")
    print(f"    Lemmatization : {str(lemma)}")
    p = Preprocessor(vocab_path)
    preprocessed = p.preprocess(corpus_path, lemma = lemma)
    concepts = tuple(preprocessed.keys())
    bows = tuple([preprocessed[bow] for bow in preprocessed])
    terms = tuple(set([word for bow in bows for word in bow]))
    print(f"Finished preprocessing: ")
    print(f"    {len(concepts)} concepts")
    print(f"    {len(terms)} individual terms")
    print(f"Computing ESA-matrix of size {len(concepts)}x{len(terms)} ...")
    mat = ESAMatrix(terms, concepts, bows)
    print(f"Writing matrix to {matrix_path} ...")
    pickle.dump(mat, open(matrix_path, "wb"))
    print(f"Finished")

if __name__ == "__main__":
    main()
