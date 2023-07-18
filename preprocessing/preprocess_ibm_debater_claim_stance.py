import pandas as pd
from conf.configuration import *
from mylogging.mylogging import *
from preprocessing.utils import *

def preprocess_corpus():
    dataset='ibm-debater-claim-stance'
    setup_logging(f"../logs/{dataset}.log")
    preprocess_document_topic(dataset,'claims.claimOriginalText','topicTarget')

preprocess_corpus()