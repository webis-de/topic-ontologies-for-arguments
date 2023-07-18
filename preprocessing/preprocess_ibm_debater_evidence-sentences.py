from conf.configuration import *
import pandas as pd
import csv
import hashlib
from utils import *

def preprocess_subset(part):
    path_subset = get_path_source_part('ibm-debater-evidence-sentences', part)
    df = pd.read_csv(path_subset,sep=",",encoding="utf-8")
    documents = list(df['candidate'])
    topics=list(df['the concept of the topic'])
    return documents,topics


def preprocess():
    path_preprocessed_arguments = get_path_preprocessed_arguments("ibm-debater-evidence-sentences")
    path_preprocessed_topics = get_path_preprocessed_topics("ibm-debater-evidence-sentences")
    path_argument_topics=get_path_argument_topic('ibm-debater-evidence-sentences')
    arguments=[]
    topics=[]
    arguments_training, topics_training = preprocess_subset('training')
    arguments_test, topics_test = preprocess_subset('test')

    arguments.extend(arguments_training)
    arguments.extend(arguments_test)


    topics.extend(topics_training)
    topics.extend(topics_test)
    uniqe_topics = list(set(topics))
    topics_df =pd.DataFrame({"topic":uniqe_topics,"topic-id":range(0,len(uniqe_topics))})
    topics_df.to_csv(path_preprocessed_topics,sep=",",encoding="utf-8",index=False)

    all_ids = range(0,len(arguments))
    corpora_df = pd.DataFrame({"argument":arguments,"argument-id":all_ids,"topic":topics})

    corpora_df=corpora_df.merge(topics_df,on='topic')
    corpora_df ['argument']=corpora_df .apply((lambda row: drop_separator(row['argument'],"\",\"")),axis=1)
    corpora_df.to_csv(path_preprocessed_arguments,quotechar='"',sep=",",quoting=csv.QUOTE_ALL, columns=['argument-id','argument'],encoding="utf-8",index=False)

    corpora_df.to_csv(path_argument_topics,quotechar='"',sep=",",quoting=csv.QUOTE_ALL,encoding="utf-8", \
                              columns=['argument-id','topic-id'],index=False)
def extract_topics_part(part):
    path_subset = get_path_source_part('ibm-debater-evidence-sentences', part)
    df_arguments = pd.read_csv(path_subset,sep=",",encoding="utf-8")
    df_arguments['argument-hash']=df_arguments.apply(lambda argument: hashlib.md5(argument['candidate'].encode()).hexdigest(),axis=1)

    df_arguments=df_arguments[['argument-hash','the concept of the topic']]
    df_arguments.rename(columns={'the concept of the topic':'topic'}, inplace=True)
    return df_arguments

def update_topic_entries():
    path_argument_topics=get_path_argument_topic('ibm-debater-evidence-sentences')
    df_argument_topics= pd.read_csv(path_argument_topics,sep=",",quotechar='"',encoding="utf-8")
    path_topics = get_path_preprocessed_topics("ibm-debater-evidence-sentences")
    df_topics=pd.read_csv(path_topics,sep=",",encoding="utf-8")
    path_topics_original=path_topics.replace(".csv","-05-01-2021.csv")# the file is now here preprocessed-topics-ibm-debater-evidence-sentences.csv
    df_topics_original=pd.read_csv(path_topics_original,sep=",",encoding="utf-8")
    df_argument_topics=df_argument_topics.merge(df_topics,on='topic-id')
    df_argument_topics=df_argument_topics[['argument-id','topic']]
    df_argument_topics=df_argument_topics.merge(df_topics_original,on='topic')
    df_argument_topics=df_argument_topics[['argument-id','topic-id']]
    df_argument_topics.to_csv(path_argument_topics,quotechar='"',sep=",",quoting=csv.QUOTE_ALL,encoding="utf-8", \
                              columns=['argument-id','topic-id'],\
                              index=False)



#preprocess()
#update_topic_entries()