from conf.configuration import *
import pandas as pd
from preprocessing.utils import *
def preprocess():
    dataset = "arguments-moderation"
    path_source =get_path_source(dataset)
    df=pd.read_csv(path_source,sep="\t")
    df.info()
    documents = df["CLEANEDCOMMENT"]
    document_ids = df["UNIQUEID"]

    topics = df["UNIQUEID"].apply(lambda x: x.split("_")[1])
    unique_topics = df["UNIQUEID"].apply(lambda x: x.split("_")[1]).unique()
    topic_ids = range(0,len(unique_topics))

    df_topics = pd.DataFrame({"topic-id": topic_ids, "topic": unique_topics})
    path_topics = get_path_preprocessed_topics(dataset)
    save_topics(df_topics, path_topics)

    df_documents = pd.DataFrame({"document-id": document_ids, "document":documents, "topic":topics})
    df_documents_topic = df_documents.merge(df_topics,on="topic")
    path_documents = get_path_preprocessed_documents(dataset)
    path_document_topics = get_path_document_topic(dataset)
    clean_documents(df_documents)
    save_documents(df_documents, path_documents)
    save_document_topic(df_documents_topic,path_document_topics)


preprocess()