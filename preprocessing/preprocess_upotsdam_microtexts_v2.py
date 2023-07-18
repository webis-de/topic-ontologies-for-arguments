import pandas as pd
import csv
from conf.configuration import *
from lxml import etree
from collections import Counter
from utils import *
def extract_topic(path):
    tree=etree.parse(path).getroot()
    if 'topic_id' not in tree.attrib:
        return None
    else:
        return tree.attrib['topic_id']

def read_file(path):
    file = open(path,encoding='utf-8',errors="ignore")
    return " ".join(file)

def preprocess():
    corpus_path = get_path_source("upotsdam-arg-microtexts-v2")
    preprocessed_documents_path = get_path_preprocessed_documents("upotsdam-arg-microtexts-v2")
    path_topics = get_path_preprocessed_topics('upotsdam-arg-microtexts-v2')
    path_document_topic=get_path_document_topic('upotsdam-arg-microtexts-v2')
    documents =[]
    document_ids = []
    topics=[]
    for root,dirs,files in os.walk(corpus_path):
        for file_name in files:
            if file_name.endswith(".txt"):
                file_path = os.path.join(root,file_name)
                xml_path = os.path.join(root,file_name.replace("txt","xml"))
                topic =extract_topic(xml_path)
                topics.append(topic)
                document = read_file(file_path)
                documents.append(document)
                document_ids.append(file_name.replace('.txt',''))
    topic_counter=Counter(topics)
    print(topic_counter)
    unique_topics = [topic for topic in topic_counter if topic !=None ]
    df_topics = pd.DataFrame({'topic':unique_topics,'topic-id':range(0,len(unique_topics))})
    df_topics.to_csv(path_topics,sep=",",encoding="utf-8",columns=['topic-id','topic'],index=False)

    df_dataset = pd.DataFrame({"document-id":document_ids,"document":documents,'topic':topics})
    df_dataset['document']=df_dataset.apply((lambda row: drop_separator(row['document'],"\",\"")),axis=1)
    df_dataset.to_csv(preprocessed_documents_path,quotechar='"',sep=",",quoting=csv.QUOTE_ALL,encoding="utf-8", \
                      columns=['document-id','document'],index=False)

    df_dataset=df_dataset.merge(df_topics, on='topic')
    df_dataset.to_csv(path_document_topic,quotechar='"',sep=",",quoting=csv.QUOTE_ALL,encoding="utf-8", \
                      columns=['document-id','topic-id'],index=False)

preprocess()