
import pandas as pd
import re
import csv
from conf.configuration import *
import copy
import pandas as pd
from difflib import SequenceMatcher

def clean_documents(df):
    df['document']=df['document'].apply(lambda document: document.strip().replace('\n',' ').replace('\t',' ').replace("\""," ").replace("\r"," ").replace(u'¶'," "))
    df['document']=df['document'].apply(lambda document:re.sub(r'\s+',' ',document))
    df['document']=df['document'].apply(lambda document:re.sub(r'<.*?>',' ',document))

    return df


def save_topics(df_topics,path_topics):
    df_topics.to_csv(path_topics,sep=",",encoding="utf-8",columns=['topic-id','topic'],index=False)


def save_document_topic(df_document_topic,path_document_topic):
    df_document_topic.to_csv(path_document_topic,quotechar='"',sep=",",quoting=csv.QUOTE_ALL,encoding="utf-8", \
                      columns=['document-id','topic-id'],index=False)


def save_documents(df_documents, path, columns=['document-id', 'document', ]):
    if columns!=None:
        df_documents.to_csv(path,quotechar='"',sep=",",quoting=csv.QUOTE_ALL, \
                        columns=columns,encoding="utf-8",index=False)
    else:
        df_documents.to_csv(path,quotechar='"',sep=",",quoting=csv.QUOTE_ALL, \
                  encoding="utf-8",index=False)


def preprocess_document_topic(dataset,document_label,topic_label,sep=','):

    path_source=get_path_source(dataset)
    path_topics=get_path_preprocessed_topics(dataset)
    path_preprocessed_documents=get_path_preprocessed_documents(dataset)
    path_document_topics=get_path_document_topic(dataset)
    df=pd.read_csv(path_source,sep=sep,encoding="utf-8")
    unpacked_topics={'topic':[],'topic-id':[]}
    unpacked_topics['topic']=sorted(df[topic_label].unique())
    topics_count=len(unpacked_topics['topic'])
    unpacked_topics['topic-id']=range(0,topics_count)
    df_topics=pd.DataFrame(unpacked_topics)
    save_topics(df_topics,path_topics)

    unpacked_documents={}
    unpacked_documents['document']=df[document_label].values
    unpacked_documents['topic']=df[topic_label].values
    unpacked_documents['document-id']=range(0,len(unpacked_documents['document']))
    df_documents=pd.DataFrame(unpacked_documents)
    df_documents=df_documents.merge(df_topics,on='topic')
    df_documents=clean_documents(df_documents)

    save_documents(df_documents,path_preprocessed_documents)
    save_document_topic(df_documents,path_document_topics)

def preprocess_document_topic_parts(dataset,parts,topic_labels,document_labels,sep=','):

    path_topics=get_path_preprocessed_topics(dataset)
    path_preprocessed_documents=get_path_preprocessed_documents(dataset)
    path_document_topics=get_path_document_topic(dataset)
    unpacked_topics={'topic':[],'topic-id':[]}
    unpacked_documents={'document':[],'topic':[]}
    for part,topic_label,document_label in zip(parts,topic_labels,document_labels):
        path_source_part=get_path_source_part(dataset,part)
        df=pd.read_csv(path_source_part,sep=sep,encoding="utf-8")
        unpacked_topics['topic'].extend(df[topic_label].unique())
        unpacked_documents['document'].extend(df[document_label].values)
        unpacked_documents['topic'].extend(df[topic_label].values)

    unpacked_topics['topic']=unique(copy.deepcopy(unpacked_topics['topic']))
    topics_count=len(unpacked_topics['topic'])
    unpacked_topics['topic-id']=range(0,topics_count)
    df_topics=pd.DataFrame(unpacked_topics)
    save_topics(df_topics,path_topics)

    document_count=len(unpacked_documents['document'])
    unpacked_documents['document-id']=range(0,document_count)
    df_documents=pd.DataFrame(unpacked_documents)
    df_documents=df_documents.merge(df_topics,on='topic')
    df_documents=clean_documents(df_documents)

    save_documents(df_documents,path_preprocessed_documents)
    save_document_topic(df_documents,path_document_topics)

def unique(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


def similar(a,b):
    return SequenceMatcher(None,a,b).ratio()

def fuzzy_merge_topic_ids(df_documents,df_topics,):
    df_documents['topic-id']=-1
    for d_i,d_row in df_documents.iterrows():
        best_similarity=0
        for topic_i,topic_row in df_topics.iterrows():
            similarity=similar(d_row['topic'],topic_row['topic'])
            if similarity>best_similarity :
                topic_id= topic_row['topic-id']
                df_documents.loc[d_i,'topic-id']=topic_id
                best_similarity=similarity
    return df_documents

def drop_separator(text,sep):
    return text.replace(sep,"")