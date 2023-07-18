from conf.configuration import *
import pandas as pd
import csv
from utils import *
def read_file(file_path):
    file = open(file_path,'r',encoding='utf-8',errors="ignore")
    lines =[]
    for line in file:
        l = line.replace('\n','').replace('\t','')
        lines.append(l)
    return " ".join(lines)

def load_topics():
    path_topics=get_path_preprocessed_topics('ibm-debater-claim-evidence-acl')
    df_topics=pd.read_csv(path_topics,sep=",",encoding="utf-8")
    return df_topics

def generate_document_topic(df_documents):
    path_evidence=get_path_source_part('ibm-debater-claim-evidence-acl', 'evidence')
    df_topics=load_topics()
    df_evidence=pd.read_csv(path_evidence,sep=",",encoding="utf-8")
    df_evidence=df_evidence[['Topic','Article']]
    df_evidence.drop_duplicates(['Topic','Article'],inplace=True)
    df_evidence.rename(columns={'Topic':'topic','Article':'topic-key'},inplace=True)
    df_documents=df_documents.merge(df_evidence,on='topic-key')

    df_documents=df_documents.merge(df_topics,on='topic')
    #df_documents=df_documents[['topic-id','document','document-id']]
    return df_documents

def preprocess():
    path_corpus_ascii = get_path_source_part("ibm-debater-claim-evidence-acl", "documents")
    path_preprocessed_documents = get_path_preprocessed_documents('ibm-debater-claim-evidence-acl')
    path_document_topic=get_path_document_topic('ibm-debater-claim-evidence-acl')
    for root,dirs,files in os.walk(path_corpus_ascii):
        documents = []
        for file_name in files:
            file_path = os.path.join(root,file_name)
            file_content = read_file(file_path)
            documents.append(file_content)
    topic_keys=[file.replace('_',' ') for file in files]
    df_documents = pd.DataFrame({"document":documents,"document-id":files,'topic-key':topic_keys})

    df_documents['document']=df_documents.apply((lambda row: drop_separator(row['document'],"\",\"")),axis=1)
    df_documents.to_csv(path_preprocessed_documents,quotechar='"',sep=",",quoting=csv.QUOTE_ALL,encoding="utf-8",\
            columns=['document-id','document'],index=False)
    df_document_topic=generate_document_topic(df_documents)
    df_document_topic.to_csv(path_document_topic,quotechar='"',sep=",",quoting=csv.QUOTE_ALL,encoding="utf-8", \
                             columns=['document-id','topic-id'],index=False)
    return documents,files

def extract_topics():
    path_topics=get_path_preprocessed_topics('ibm-debater-claim-evidence-acl')
    path_evidence=get_path_source_part('ibm-debater-claim-evidence-acl', 'evidence')
    df_evidence=pd.read_csv(path_evidence,sep=",",encoding="utf-8")
    df_topics=df_evidence[['Topic']]
    df_topics=df_topics.drop_duplicates(['Topic'])
    df_topics.rename(columns={'Topic':'topic'},inplace=True)
    df_topics['topic-id']=range(0,df_topics.shape[0])
    df_topics.to_csv(path_topics,columns={'topic-id','topic'},sep=",",encoding="utf-8",index=False)


#extract_topics()
preprocess()