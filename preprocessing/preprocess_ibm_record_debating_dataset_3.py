from conf.configuration import *
import pandas as pd
import csv
import re
from utils import *
def read_file(file_path):
    file = open(file_path,'r')
    cleanded_lines = [line.replace("\t","").replace("\n","") for line in file]
    return " ".join(cleanded_lines)

def extract_topic(filename):
    indices = [m.start() for m in re.finditer("_",filename)]
    second_index=indices[1]
    third_index=indices[2]
    topic= filename[second_index+1:third_index].replace("-"," ")
    if topic == 'transfat':
        return 'trans fat'
    if topic == 'windpower':
        return 'wind power'
    if topic =='cocaleaf':
        return 'coca leaf'
    return topic

def preprocess():
    path_corpus = get_path_source("ibm-record-debating-dataset-v3")
    path_preprocessed_documents = get_path_preprocessed_documents("ibm-record-debating-dataset-v3")
    path_preprocessed_topics = get_path_preprocessed_topics('ibm-record-debating-dataset-v3')

    for root,dirs,files in os.walk(path_corpus):
        documents = []
        for file_name in files:
            file_path = os.path.join(root,file_name)
            file_content = read_file(file_path)
            documents.append(file_content)
    cleaned_files= list(map(lambda x: x.replace(".asr.txt",""),files))

    topics = list(map(lambda x: extract_topic(x),files))
    topics = list(set(topics))

    #topics_df=pd.DataFrame({'topic':topics,'topic-id':range(0,len(topics))})
    #topics_df.to_csv(path_preprocessed_topics,sep=",",encoding="utf-8",index=False)

    corpora_df = pd.DataFrame({"document":documents,"document-id":cleaned_files})
    corpora_df['document']=corpora_df.apply((lambda row: drop_separator(row['document'],"\",\"")),axis=1)
    corpora_df.to_csv(path_preprocessed_documents,columns=['document-id','document'],quotechar='"',sep=",",quoting=csv.QUOTE_ALL,encoding="utf-8",index=False)

def add_topic_ids():
    path_preprocessed_documents = get_path_preprocessed_documents("ibm-record-debating-dataset-v3")
    path_preprocessed_topics = get_path_preprocessed_topics('ibm-record-debating-dataset-v3')
    path_document_topic=get_path_document_topic('ibm-record-debating-dataset-v3')
    df_topics = pd.read_csv(path_preprocessed_topics,sep=",", encoding="utf-8")

    df_documents = pd.read_csv(path_preprocessed_documents,quotechar='"',sep=",",encoding="utf-8")
    df_documents['topic']=df_documents.apply(lambda document: extract_topic(document['document-id']) ,axis=1)
    df_documents=df_documents.merge(df_topics,on='topic')
    df_documents.to_csv(path_document_topic,quotechar='"',sep=",",quoting=csv.QUOTE_ALL,encoding="utf-8", \
                        columns=['document-id','topic-id'],index=False)

preprocess()

#add_topic_ids()