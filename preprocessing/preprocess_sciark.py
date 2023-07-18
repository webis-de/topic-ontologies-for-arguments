import pandas as pd
import os
import json

from conf.configuration import *
from preprocessing.utils import *


def preprocess():
    dataset = "sciark"
    topic_map = {
        3: "good health and well-being",
        5: "gender equality",
        7: "affordable and clean energy",
        10: "reduce inequalities",
        12: "responsible consumption",
        13: "climate action"
    }
    df_topics = pd.DataFrame({"topic-id": topic_map.keys(), "topic": topic_map.values()})
    path_topics = get_path_preprocessed_topics(dataset)
    save_topics(df_topics,path_topics)
    print(df_topics)
    path_source = get_path_source(dataset)
    all_topics = []
    all_docs = []
    all_doc_ids = []
    all_topic_ids = []
    with open(path_source) as file:
        data = json.load(file)
        for key in data:
            doc_obj = data[key]
            topic_id = int(doc_obj["sdg"])
            topic = doc_obj["sdg"]
            document = " ".join(doc_obj["sentences"])
            all_docs.append(document)
            all_topics.append(topic)
            all_doc_ids.append(key)
            all_topic_ids.append(topic_id)

    df_documents = pd.DataFrame({"document": all_docs, "document-id": all_doc_ids, "topic-id": all_topic_ids})
    df_documents["document-id"] = df_documents["document-id"].apply(lambda x: x.replace(".txt", ""))
    clean_documents(df_documents)
    path_documents = get_path_preprocessed_documents(dataset)
    path_document_topics = get_path_document_topic(dataset)
    save_documents(df_documents, path_documents)
    save_document_topic(df_documents, path_document_topics)
preprocess()