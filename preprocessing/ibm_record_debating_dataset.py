import pandas as pd
from conf.configuration import *
import re

from mylogging.mylogging import *
from preprocessing.utils import *
def read_file(file_path):
    file = open(file_path,'r')

    return " ".join(file)
def extract_topic(filename):
    indices = [m.start() for m in re.finditer("_",filename)]
    second_index=indices[1]
    third_index=indices[2]
    topic= filename[second_index+1:third_index].replace("-"," ")
    return topic


def extract_topics(files,file_ending_pattern):

    cleaned_files= list(map(lambda x: x.replace(file_ending_pattern,""),files))
    topics=[extract_topic(filename) for filename in cleaned_files]
    topics=sorted(topics)
    unique_topics=unique(topics)
    topics_count=len(unique_topics)
    topic_ids=range(0,topics_count)
    df_topics=pd.DataFrame({'topic':unique_topics,'topic-id':topic_ids})
    return df_topics, topics


def preprocess_debating_dataset(dataset,file_ending_pattern):
    setup_logging(f"../logs/{dataset}.log")
    path_corpus = get_path_source(dataset)
    path_preprocessed_documents = get_path_preprocessed_documents(dataset)
    path_document_topic=get_path_document_topic(dataset)
    path_preprocessed_topics = get_path_preprocessed_topics(dataset)

    for root,dirs,files in os.walk(path_corpus):
        documents = []
        for i,file_name in enumerate(files):
            file_path = os.path.join(root,file_name)
            file_content = read_file(file_path)
            documents.append(file_content)
            log(f"preprocessing {file_name}")
            log_status(i,len(files),True)

    cleaned_files= list(map(lambda x: x.replace(file_ending_pattern,""),files))
    sorted_documents=sorted(zip(cleaned_files,documents),key=lambda topic_document:extract_topic(topic_document[0]))
    cleaned_files,documents=zip(*sorted_documents)

    df_topics,topics=extract_topics(files,file_ending_pattern)
    save_topics(df_topics,path_preprocessed_topics)

    df_documents=pd.DataFrame({'document':documents,'topic':topics,'document-id':cleaned_files})
    df_documents=clean_documents(df_documents)
    df_documents=df_documents.merge(df_topics,on='topic')
    save_documents(df_documents,path_preprocessed_documents)
    save_document_topic(df_documents,path_document_topic)

