import pandas as pd
from conf.configuration import *
from preprocessing.utils import *
from mylogging.mylogging import *

def preprocess_corpus():
    dataset='ukp-aspect'
    path_source=get_path_source(dataset)
    path_preprocessed_documents=get_path_preprocessed_documents(dataset)
    path_topics=get_path_preprocessed_topics(dataset)
    path_document_topics=get_path_document_topic(dataset)

    df=pd.read_csv(path_source,sep="\t",encoding="utf-8")


    unpacked_topics={'topic':[],'topic-id':[]}
    unpacked_topics['topic']=sorted(df['topic'].unique())
    topics_count=len(unpacked_topics['topic'])
    unpacked_topics['topic-id']=range(0,topics_count)
    df_topics=pd.DataFrame(unpacked_topics)
    save_topics(df_topics,path_topics)

    unpacked_documents={'document':[],'topic':[],'document-id':[]}
    unpacked_documents['document'].extend(df['sentence_1'].values)
    unpacked_documents['topic'].extend(df['topic'].values)
    unpacked_documents['document'].extend(df['sentence_2'].values)
    unpacked_documents['topic'].extend(df['topic'].values)

    documents_count = len(unpacked_documents['document'])
    unpacked_documents['document-id']=range(0,documents_count)

    df_documents=pd.DataFrame(unpacked_documents)
    df_documents=df_documents.merge(df_topics,on='topic')
    df_documents=clean_documents(df_documents)
    save_documents(df_documents,path_preprocessed_documents)
    save_document_topic(df_documents,path_document_topics)

preprocess_corpus()