import os
import re
import pandas as pd
from conf.configuration import *

from utils import *

def parse_topic(token):
    tokens=token.split("-")
    topic = tokens[0]
    pattern="\d*$"
    cleaned_topic=re.sub(pattern,"",topic)
    return cleaned_topic

def preprocess_corpus():
    path_source = get_path_source('webis-debate-16')
    path_preprocessed_documents = get_path_preprocessed_documents('webis-debate-16')
    path_preprocessed_topics = get_path_preprocessed_topics('webis-debate-16')

    path_document_topics= get_path_document_topic('webis-debate-16')
    topic_ids=[]
    documents=[]

    file_names = sorted(os.listdir(path_source))
    cleaned_files = [file.replace(".txt","") for file in file_names]
    topics = [parse_topic(file) for file in cleaned_files]
    unique_topics = unique(topics)

    unique_topic_ids = range(0,len(unique_topics))
    unique_topic_id_map= dict(zip(unique_topics,unique_topic_ids))

    df_topics=pd.DataFrame({'topic-id':unique_topic_ids,'topic':unique_topics})
    df_topics.to_csv(path_preprocessed_topics,sep=",",quotechar='"',quoting=csv.QUOTE_ALL,encoding="utf-8",index=False)

    for file_name in file_names:
        path_file=os.path.join(path_source,file_name)
        doc=""
        with open(path_file) as file:
            for line in file:
                tokens=line.split("\t")
                doc=doc+ " " +tokens[1]
        documents.append(doc)
        topic=parse_topic(file_name.replace(".txt",""))
        id = unique_topic_id_map[topic]
        topic_ids.append(id)

    df_documents=pd.DataFrame({'document-id':cleaned_files,'document':documents,'topic-id':topic_ids})
    df_documents=clean_documents(df_documents)
    df_documents.to_csv(path_preprocessed_documents,sep=",",quotechar='"',quoting=csv.QUOTE_ALL,encoding="utf-8",columns=['document-id','document'],index=False)
    df_documents.to_csv(path_document_topics,sep=",",quotechar='"',quoting=csv.QUOTE_ALL,encoding="utf-8",columns=['document-id','topic-id'],index=False)

preprocess_corpus()
