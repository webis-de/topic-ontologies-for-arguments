#!pip install sqlalchemy pymysql
from sqlalchemy import create_engine
import pandas as pd
from conf.configuration import *
from utils import *


databases= ['createdebate','fourforums','convinceme']
#databases= ['createdebate','convinceme']

dataset='iac2'
def create_connections():
    connections={}
    for database in databases:
        db_connection_str = f'mysql+pymysql://yamenajjour:STaAEJUlfv@127.0.0.1:3306/{database}'
        db_connection = create_engine(db_connection_str)
        connections[database]=db_connection
    return connections

def preprocess_documents(database,connections):
    connection = connections[database]
    df = pd.read_sql('SELECT discussion_id, GROUP_CONCAT(text separator" ") as discussion_text FROM post natural join discussion natural join text group by discussion_id;', con=connection)
    df['document-id']=df.apply(lambda x: database+"_"+str(x['discussion_id']),axis=1)
    df.rename(columns={'discussion_text':'document'},inplace=True)
    df=df[['document-id','document']]
    df=clean_documents(df)
    return df


def preprocess_topics(database,connections):
    connection = connections[database]
    df = pd.read_sql('SELECT topic_id,topic FROM topic',con=connection)
    df.rename(columns={'topic_id':'topic-id'},inplace=True)
    df=df.sort_values('topic-id',inplace=True)
    return df

def generate_document_topics(database,connections):
    connection = connections[database]
    df = pd.read_sql('SELECT discussion_id,topic_id FROM discussion_topic',con=connection)
    df['document-id']=df.apply(lambda x: database+"_"+str(x['discussion_id']),axis=1)
    df.rename(columns={'topic_id':'topic-id'},inplace=True)
    df=df[['document-id','topic-id']]
    return df

def preprocess_all_databases():
    connections= create_connections()
    all_documents=[]

    all_document_topics=[]
    for database in databases:

        df_documents=preprocess_documents(database,connections)

        df_document_topics=generate_document_topics(database,connections)

        all_documents.append(df_documents)

        all_document_topics.append(df_document_topics)

    path_topics = get_path_preprocessed_topics(dataset)
    path_preprocessed_documents=get_path_preprocessed_documents(dataset)
    path_document_topics= get_path_document_topic(dataset)
    df_all_documents=pd.concat(all_documents)
    df_all_topics=preprocess_topics(databases[0],connections)
    df_all_document_topics=pd.concat(all_document_topics)
    df_all_documents.to_csv(path_preprocessed_documents,sep=",",quotechar='"',quoting=csv.QUOTE_ALL,encoding="utf-8",index=False)
    df_all_topics.to_csv(path_topics,sep=",",quotechar='"',quoting=csv.QUOTE_ALL,encoding="utf-8",index=False)
    df_all_document_topics.to_csv(path_document_topics,sep=",",quotechar='"',quoting=csv.QUOTE_ALL,encoding="utf-8",index=False)

preprocess_all_databases()

