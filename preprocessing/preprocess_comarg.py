import pandas as pd
import csv
from utils import *
from docutils.nodes import topic

from conf.configuration import *
from lxml import etree
from collections import Counter

def extract_topic(file):
    topic_shortcut = file.replace(".xml","")
    if topic_shortcut == 'GM':
        return "gay marriage",0
    else:
        return "under god in pledge",1

def read_file(path):
    file = open(path,encoding='utf-8',errors="ignore")
    return " ".join(file)


def extract_argument_pairs(child):
    argument1=child[0][0].text
    argument2=child[1][0].text
    return argument1, argument2

def extract_argument_ids(child):
    argument_id=child.get("id")
    print(argument_id)
    return argument_id +"_1", argument_id +"_2"

def preprocess():
    dataset='com-arg'
    corpus_path = get_path_source(dataset)
    preprocessed_documents_path = get_path_preprocessed_documents(dataset)
    path_topics = get_path_preprocessed_topics(dataset)
    path_document_topic=get_path_document_topic(dataset)
    arguments =[]
    document_ids = []
    topic_ids=[]
    unique_topic_ids=[]
    unique_topics=[]
    for root,dirs,files in os.walk(corpus_path):
        for file_name in files:
            if file_name.endswith(".xml"):
                file_path = os.path.join(root,file_name)
                tree=etree.parse(file_path).getroot()
                topic,topic_id = extract_topic(file_name)
                unique_topic_ids.append(topic_id)
                unique_topics.append(topic)
                for child in tree:
                    argument1, argument2 = extract_argument_pairs(child)
                    argument1_id, argument2_id = extract_argument_ids(child)
                    arguments.append(argument1)
                    arguments.append(argument2)
                    document_ids.append(argument1_id)
                    document_ids.append(argument2_id)
                    topic_ids.append(topic_id)
                    topic_ids.append(topic_id)


    df_topics = pd.DataFrame({'topic':unique_topics,'topic-id':unique_topic_ids })
    df_topics.to_csv(path_topics,sep=",",encoding="utf-8",columns=['topic-id','topic'],index=False)

    df_dataset = pd.DataFrame({"document-id":document_ids,"document":arguments,'topic-id':topic_ids})
    df_dataset=clean_documents(df_dataset)
    df_dataset['document']=df_dataset.apply((lambda row: drop_separator(row['document'],"\",\"")),axis=1)
    df_dataset.to_csv(preprocessed_documents_path,quotechar='"',sep=",",quoting=csv.QUOTE_ALL,encoding="utf-8", \
                      columns=['document-id','document'],index=False)


    df_dataset.to_csv(path_document_topic,quotechar='"',sep=",",quoting=csv.QUOTE_ALL,encoding="utf-8", \
                      columns=['document-id','topic-id'],index=False)

preprocess()