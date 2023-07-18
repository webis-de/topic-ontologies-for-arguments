import pandas as pd
import csv
from conf.configuration import *
import hashlib
from utils import *
def preprocess_part(part):
    path_evidence_quality_source_part = get_path_source_part('ibm-debater-evidence-quality', part)
    dataframe_evidence_quality_part = pd.read_csv(path_evidence_quality_source_part,sep=",",encoding='utf-8')
    topics=dataframe_evidence_quality_part['topic']

    all_arguments = []
    all_topics = []

    arguments_1 = list(dataframe_evidence_quality_part['evidence_1'])
    arguments_2 = list(dataframe_evidence_quality_part['evidence_2'])

    all_arguments.extend(arguments_1)
    all_arguments.extend(arguments_2)
    all_topics.extend(topics)
    all_topics.extend(topics)

    return all_arguments,all_topics

def preprocess():
    arguments= []
    topics=[]
    path_evidence_quality_topics = get_path_preprocessed_topics('ibm-debater-evidence-quality')
    path_argument_topic =get_path_argument_topic('ibm-debater-evidence-quality')
    path_evidence_quality_preprocessed = get_path_preprocessed_arguments('ibm-debater-evidence-quality')
    training_arguments,training_topics = preprocess_part('training')
    test_arguments,test_topics = preprocess_part('test')

    arguments.extend(training_arguments)
    arguments.extend(test_arguments)

    topics.extend(training_topics)
    topics.extend(test_topics)
    unique_topics=list(set(list(topics)))
    topic_ids = range(0,len(unique_topics))

    df_topics = pd.DataFrame({'topic-id':topic_ids,'topic':unique_topics})
    df_topics.to_csv(path_evidence_quality_topics,sep=",",encoding="utf-8",index=False)

    ids = list(range(0,len(arguments)))


    dataframe_arguments = pd.DataFrame({"argument-id":ids,'argument':arguments,'topic':topics})
    dataframe_arguments=dataframe_arguments.merge(df_topics,on="topic")
    dataframe_arguments ['argument']=dataframe_arguments .apply((lambda row: drop_separator(row['argument'],"\",\"")),axis=1)

    dataframe_arguments.to_csv(path_evidence_quality_preprocessed,quotechar='"',sep=",",quoting=csv.QUOTE_ALL,columns=['argument-id','argument'],encoding="utf-8",index=False)
    dataframe_arguments.to_csv(path_argument_topic,quotechar='"',sep=",",quoting=csv.QUOTE_ALL,columns=['argument-id','topic-id'],encoding="utf-8",index=False)


def update_topic_entries():
    path_argument_topics=get_path_argument_topic('ibm-debater-evidence-quality')
    df_argument_topics= pd.read_csv(path_argument_topics,sep=",",quotechar='"',encoding="utf-8")
    path_topics = get_path_preprocessed_topics("ibm-debater-evidence-quality")
    df_topics=pd.read_csv(path_topics,sep=",",encoding="utf-8")
    path_topics_original=path_topics.replace(".csv","-01-05.csv")# this file is now preprocessed-topics-ibm-debater-evidence-quality.csv 01-05-2021
    df_topics_original=pd.read_csv(path_topics_original,sep=",",encoding="utf-8")
    df_argument_topics=df_argument_topics.merge(df_topics,on='topic-id')
    df_argument_topics=df_argument_topics[['argument-id','topic']]
    df_argument_topics=df_argument_topics.merge(df_topics_original,on='topic')
    df_argument_topics=df_argument_topics[['argument-id','topic-id']]
    df_argument_topics.to_csv(path_argument_topics,quotechar='"',sep=",",quoting=csv.QUOTE_ALL,encoding="utf-8", \
                              columns=['argument-id','topic-id'], \
                              index=False)







preprocess()
#update_topic_entries()