from conf.configuration import *
from preprocessing.utils import *
from mylogging.mylogging import *

def preprocess_corpus():
    dataset='ibm-debater-argumentative-sentences'
    setup_logging(f"../logs/{dataset}.log")
    preprocess_document_topic(dataset,'sentence','topic')

setup_logging('../logs/ibm-debater-argumentative-sentences.log')
preprocess_corpus()