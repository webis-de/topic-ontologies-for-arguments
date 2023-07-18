from preprocessing.utils import *
from mylogging.mylogging import *

def preprocess_corpus():
    dataset='ibm-debater-multilingual-argument-mining'
    setup_logging(f"../logs/{dataset}.log")
    parts=['evidence','argument']
    topic_labels=['topic_EN']*2
    document_labels=['sentence_EN','argument_EN']
    preprocess_document_topic_parts(dataset,parts,topic_labels,document_labels)

preprocess_corpus()