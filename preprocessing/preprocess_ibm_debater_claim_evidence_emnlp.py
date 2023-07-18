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
    path_topics=get_path_preprocessed_topics('ibm-debater-claim-evidence-emnlp')
    df_topics=pd.read_csv(path_topics,sep=",",encoding="utf-8")
    return df_topics

def get_articles():
    path_list = get_path_source_part("ibm-debater-claim-evidence-emnlp", "documents-list")
    articles = []
    with open(path_list,'r') as articles_list_file:
        for line in articles_list_file.readlines():
            tokens = line.split('\t')
            articles.append(tokens[2].strip())
    return articles

def generate_document_topics(df_documents):
    path_list = get_path_source_part("ibm-debater-claim-evidence-emnlp", "documents-list")
    df_topics=load_topics()
    df_document_list=pd.read_csv(path_list,sep="\t",encoding="utf-8")
    df_document_list=df_document_list[['Topic','article Id']]
    df_document_list.rename(columns={'article Id':'topic-key','Topic':'topic'},inplace=True)
    df_documents_topics=df_documents.merge(df_document_list,on='topic-key')
    df_documents_topics=df_documents_topics.merge(df_topics,on='topic')
    df_documents_topics=df_documents_topics[['document-id','document','topic-id']]
    return df_documents_topics
def preprocess():
    articles = get_articles()
    path_corpus_ascii = get_path_source_part("ibm-debater-claim-evidence-emnlp", "documents")
    path_preprocessed_documents = get_path_preprocessed_documents('ibm-debater-claim-evidence-emnlp')
    path_document_topics=get_path_document_topic('ibm-debater-claim-evidence-emnlp')
    document_ids= []
    for root,dirs,files in os.walk(path_corpus_ascii):
        documents = []
        for file_name in files:
            article_number = file_name.replace("clean_","").replace(".txt","")
            if article_number in articles:
                file_path = os.path.join(root,file_name)
                file_content = read_file(file_path)
                document_ids.append(article_number)
                documents.append(file_content)
    topic_keys=[int(document_id) for document_id in document_ids]
    df_documents = pd.DataFrame({"document":documents,"document-id":document_ids,'topic-key':topic_keys})
    df_documents ['document']=df_documents.apply((lambda row: drop_separator(row['document'],"\",\"")),axis=1)
    df_documents.to_csv(path_preprocessed_documents,quotechar='"',sep=",",quoting=csv.QUOTE_ALL,encoding="utf-8", columns=['document-id','document'],index=False)
    df_document_topics=generate_document_topics(df_documents)

    df_document_topics.to_csv(path_document_topics,quotechar='"',sep=",",quoting=csv.QUOTE_ALL,encoding="utf-8", \
                        columns=['document-id','topic-id'],index=False)
    return documents,files

def extract_topics():
    path_topics=get_path_preprocessed_topics('ibm-debater-claim-evidence-emnlp')
    path_evidence=get_path_source_part('ibm-debater-claim-evidence-emnlp', 'motions')
    df_evidence=pd.read_csv(path_evidence,sep="\t",encoding="utf-8")
    df_topics=df_evidence[['Topic']]
    df_topics=df_topics.drop_duplicates(['Topic'])
    df_topics.rename(columns={'Topic':'topic'},inplace=True)
    df_topics=df_topics.drop_duplicates(['topic'])
    df_topics['topic-id']=range(0,df_topics.shape[0])
    df_topics.to_csv(path_topics,sep=",",encoding="utf-8",index=False)

#extract_topics()
preprocess()
#get_articles()