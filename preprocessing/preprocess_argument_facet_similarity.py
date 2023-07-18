import os

import pandas as pd
from conf.configuration import *
from utils import *

def preprocess_topic(token):
    token=token.replace(".csv","")
    token=token.replace("-"," ")
    topic_id=0
    if token =='death penalty':
        topic_id=0
    elif token =='gay marriage':
        topic_id=1
    else:
        topic_id=2
    return topic_id,token

def preprocess():
    dataset="argument-facet-similarity"

    path_source =get_path_source(dataset)
    path_topics = get_path_preprocessed_topics(dataset)
    path_preprocessed_documents=get_path_preprocessed_documents(dataset)
    path_document_topics= get_path_document_topic(dataset)
    unique_topics=[]
    unique_topic_ids=[]

    all_topic_ids=[]
    all_arguments=[]

    for file in os.listdir(path_source):
        path_file=os.path.join(path_source,file)
        print(path_file)
        topic_id,topic=preprocess_topic(file)
        unique_topics.append(topic)
        unique_topic_ids.append(topic_id)
        df=pd.read_csv(path_file,sep=",",encoding="latin-1")

        arguments=df['sentence']
        topic_ids=[topic_id for argument in arguments]
        all_arguments.extend(arguments)
        all_topic_ids.extend(topic_ids)
    all_argument_ids=list(range(0,len(all_arguments)))
    df=pd.DataFrame({'document-id':all_argument_ids,'document':all_arguments,'topic-id':all_topic_ids})
    df_documents=clean_documents(df_documents)
    df.to_csv(path_preprocessed_documents,sep=",",quotechar='"',quoting=csv.QUOTE_ALL,encoding="utf-8",columns=['document-id','document'],index=False)
    df.to_csv(path_document_topics,sep=",",quotechar='"',quoting=csv.QUOTE_ALL,encoding="utf-8",columns=['document-id','topic-id'],index=False)
    df_topics=pd.DataFrame({'topic-id':unique_topic_ids,'topic':unique_topics})
    df_topics.to_csv(path_topics,sep=",",quotechar='"',quoting=csv.QUOTE_ALL,encoding="utf-8",index=False)

preprocess()