import pandas as pd
from conf.configuration import *
from utils import *
import csv


from utils import *
def preproces_corpus():
    dataset='political-argumentation'
    path_preprocessed_documents = get_path_preprocessed_documents(dataset)
    path_preprocessed_topics = get_path_preprocessed_topics(dataset)
    path_document_topic=get_path_document_topic(dataset)
    path_source =get_path_source(dataset)
    df_dataset=pd.read_csv(path_source,sep="\t",encoding="utf-8")
    df_dataset=df_dataset.sort_values('topic')
    unique_topics=df_dataset['topic'].unique()
    unique_topic_ids=range(0,len(unique_topics))
    df_topics = pd.DataFrame({'topic':unique_topics,'topic-id':unique_topic_ids})
    df_topics.to_csv(path_preprocessed_topics,sep=",",encoding="utf-8",index=False)
    topic_id_map=dict(zip(unique_topics,unique_topic_ids))
    df_dataset['topic-id']=df_dataset.apply(lambda x:topic_id_map[x['topic']],axis=1)
    df_dataset['argument1_id']=df_dataset.apply(lambda x:str(x['pair_id'])+"_"+x['source_arg_1'],axis=1)
    df_dataset['argument2_id']=df_dataset.apply(lambda x:str(x['pair_id'])+"_"+x['source_arg_2'],axis=1)
    arguments=list(df_dataset['argument1'].values)
    print(df_dataset['argument2'].values[0])
    arguments.extend(df_dataset['argument2'].values)
    argument_ids=list(df_dataset['argument1_id'].values)
    argument_ids.extend(df_dataset['argument2_id'].values)
    topics_ids=list(df_dataset['topic-id'].values)
    topics_ids.extend(df_dataset['topic-id'].values)
    df_documents=pd.DataFrame({'document-id':argument_ids,'document':arguments,'topic-id':topics_ids})
    df_documents=clean_documents(df_documents)
    df_documents.to_csv(path_preprocessed_documents,sep=",",quotechar='"',quoting=csv.QUOTE_ALL,encoding="utf-8",columns=['document-id','document'],index=False)
    df_documents.to_csv(path_document_topic,sep=",",quotechar='"',quoting=csv.QUOTE_ALL,encoding="utf-8",columns=['document-id','topic-id'],index=False)




preproces_corpus()