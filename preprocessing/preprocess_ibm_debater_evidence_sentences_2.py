import pandas as pd
from conf.configuration import *
from mylogging.mylogging import *
from preprocessing.utils import *

def preprocess_corpus():
    dataset='ibm-debater-evidence-sentences-2'
    setup_logging(f"../logs/{dataset}.log")
    preprocess_document_topic(dataset,'Evidence','Dominant Concept')

preprocess_corpus()