from mylogging.mylogging import *
from preprocessing.utils import *

def preprocess_corpus():
    dataset='ibm-debater-key-point-analysis'
    setup_logging(f"../logs/{dataset}.log")
    preprocess_document_topic(dataset,'argument','topic')

preprocess_corpus()