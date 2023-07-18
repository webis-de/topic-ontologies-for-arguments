import pandas as pd
import json
import os

from conf.configuration import *
from preprocessing.utils import *
def preprocess():
    dataset = "vivesdebate"
    path_source = get_path_source(dataset)
    df_topics = pd.DataFrame({"topic": ["surrogacy"], "topic-id": [0]})
    path_topics = get_path_preprocessed_topics(dataset)
    save_topics(df_topics, path_topics)
    all_documents = []
    all_document_ids = []
    all_topic_ids = []
    for file in os.listdir(path_source):
        path_file = os.path.join(path_source, file)
        df = pd.read_csv(path_file, sep= ",")
        document = " ".join(df["ADU_EN"])
        all_documents.append(document)
        all_document_ids.append(file.replace(".csv",""))
        all_topic_ids.append(0)
    df_docs = pd.DataFrame({"document": all_documents, "document-id": all_document_ids, "topic-id": all_topic_ids})
    path_docs = get_path_preprocessed_documents(dataset)
    path_docs_topics = get_path_document_topic(dataset)
    clean_documents(df_docs)
    save_documents(df_docs, path_docs)
    save_document_topic(df_docs, path_docs_topics)

preprocess()