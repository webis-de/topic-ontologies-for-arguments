from conf.configuration import *
import pandas as pd
from preprocessing.utils import *
import os
import json


def prerocess():
    dataset = "ccsa"
    path_source = get_path_source(dataset)
    df_topics = pd.DataFrame({"topic" : ["climate change"], "topic-id": [0]})
    path_topics = get_path_preprocessed_topics(dataset)
    save_topics(df_topics,path_topics)
    with open(path_source) as file:
        docs = json.load(file)
        args = docs.keys()
        ids = range(0, len(args))
        topics = ["climate change" for _ in args]
        df = pd.DataFrame({"document-id": ids, "document": args, "topic":topics})
        path_documents = get_path_preprocessed_documents(dataset)
        path_document_topics = get_path_document_topic(dataset)
        df = df.merge(df_topics)
        clean_documents(df)
        save_documents(df, path_documents)
        save_document_topic(df, path_document_topics)
prerocess()