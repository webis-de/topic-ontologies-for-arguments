from conf.configuration import *
import pandas as pd
from preprocessing.utils import *
import os



def preprocess():
    dataset = "m-arg"
    path_topics = get_path_preprocessed_topics(dataset)
    path_documents = get_path_preprocessed_documents(dataset)
    path_document_topics = get_path_document_topic(dataset)

    pat_source = get_path_source(dataset)
    df = pd.read_csv(pat_source, sep=",")

    most_frequent_topic = df["topic"].value_counts().index[0]
    df["topic"].fillna(most_frequent_topic, inplace=True)

    unique_topics = df["topic"].unique()

    topic_ids = range(0, len(unique_topics))
    df_topics = pd.DataFrame({"topic":unique_topics, "topic-id": topic_ids})

    save_topics(df_topics, path_topics)

    all_documents = []
    topics = []
    doc_ids = []
    df["id_1"] = df["_unit_id"].apply(lambda x: str(x) + "_arg1")
    df["id_2"] = df["_unit_id"].apply(lambda x: str(x) + "_arg2")

    all_documents.extend(df["sentence_1"])
    topics.extend(df["topic"])
    doc_ids.extend(df["id_1"])

    all_documents.extend(df["sentence_2"])
    topics.extend(df["topic"])
    doc_ids.extend(df["id_2"])

    df_docs = pd.DataFrame({"document": all_documents, "document-id": doc_ids, "topic": topics})
    df_docs = pd.merge(df_docs, df_topics, on="topic")
    clean_documents(df_docs)
    save_documents(df_docs, path_documents)
    save_document_topic(df_docs, path_document_topics)

preprocess()