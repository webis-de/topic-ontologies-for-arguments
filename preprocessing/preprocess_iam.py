from conf.configuration import *
import pandas as pd
from preprocessing.utils import *
import os


def preprocess():
    dataset = "iam"
    path_source = get_path_source(dataset)
    columns = ["ph1", "topic", "document", "ph2", "ph3"]
    df = pd.read_csv(path_source, sep="\t", encoding="utf-8", names=columns,dtype={"document":str})
    df["document"] = df["document"].astype(str)
    df.info()
    print(df["document"].sample(10))
    df["document-id"] = range(0, df.shape[0])
    unique_topics = df["topic"].unique()
    unique_topic_ids = range(0, len(unique_topics))
    df_topics = pd.DataFrame({"topic": unique_topics, "topic-id": unique_topic_ids})
    path_topics = get_path_preprocessed_topics(dataset)
    save_topics(df_topics, path_topics)
    df = df.merge(df_topics, on="topic")
    clean_documents(df)
    path_documents = get_path_preprocessed_documents(dataset)
    path_document_topics = get_path_document_topic(dataset)
    save_documents(df, path_documents)
    save_document_topic(df, path_document_topics)

preprocess()

preprocess()