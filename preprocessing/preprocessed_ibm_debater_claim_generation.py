from preprocessing.utils import *
from mylogging.mylogging import *

def preprocess_corpus():
    dataset='ibm-debater-claim-generation'
    setup_logging(f"../logs/{dataset}.log")
    parts=['covid','stance']
    topic_labels=['topic']*2
    document_labels=['text']*2
    preprocess_document_topic_parts(dataset,parts,topic_labels,document_labels)

preprocess_corpus()