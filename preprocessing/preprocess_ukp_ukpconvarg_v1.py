from conf.configuration import *
import pandas as pd
import csv
import os
import re
from utils import *
def load_topics():
    path_preprocessed_topics = get_path_preprocessed_topics("ukp-ukpconvarg-v1")
    df_topics=pd.read_csv(path_preprocessed_topics,sep=",",encoding="utf-8")
    df_topics['topic']=df_topics.apply(lambda topic:topic['topic'].lower().replace("?",'').replace("-"," "),axis=1)
    df_topics['topic']=df_topics.apply(lambda topic:re.sub(r"\s+"," ",topic['topic']),axis=1)
    return df_topics

def parse_argument_id(pair_id):
    return pair_id.split("_")

def parse_argument_ids(paired_argument_ids):
    parsed_argument_ids = [parse_argument_id(pair_id) for pair_id in paired_argument_ids]
    a1_ids = [id_pair[0] for id_pair in parsed_argument_ids]
    a2_ids = [id_pair[1] for id_pair in parsed_argument_ids]
    argument_ids = []
    argument_ids.extend(a1_ids)
    argument_ids.extend(a2_ids)
    return argument_ids


def parse_debate(file_path,filename):
    debate_dataframe= pd.read_csv(file_path,sep="\t",encoding="utf-8")
    debate_arguments_1 = list(debate_dataframe['a1'])
    debate_arguments_2 = list(debate_dataframe['a2'])
    arguments =[]
    paired_argument_ids= list(debate_dataframe['#id'])

    argument_ids = parse_argument_ids(paired_argument_ids)
    arguments.extend(debate_arguments_1)
    arguments.extend(debate_arguments_2)
    topic= extract_topic(filename)
    topics = [topic for argument in arguments]

    return arguments,argument_ids,topics


def extract_topic(filename):
    _index=filename.index("_")
    topic=filename[:_index]
    topic=topic.replace("-",' ')
    return topic
def preprocess():
    path_ukp_convarg_v1 = get_path_source("ukp-ukpconvarg-v1")
    path_ukp_confvarg_v1_preprocessed = get_path_preprocessed_arguments("ukp-ukpconvarg-v1")
    path_argument_topic=get_path_argument_topic('ukp-ukpconvarg-v1')
    df_topics=load_topics()

    all_argument_ids=[]
    all_arguments=[]
    all_topics=[]

    for root,dirs,files in os.walk(path_ukp_convarg_v1):
        for file_name in files:
            file_path = os.path.join(root,file_name)
            arguments,argument_ids,topics = parse_debate(file_path,file_name)


            all_topics.extend(topics)
            all_argument_ids.extend(argument_ids)
            all_arguments.extend(arguments)


    df_ukp_conv_arg_1 = pd.DataFrame({"argument-id":all_argument_ids,"argument":all_arguments,"topic":all_topics})
    df_ukp_conv_arg_1['argument']=df_ukp_conv_arg_1.apply((lambda row: drop_separator(row['argument'],"\",\"")),axis=1)
    df_ukp_conv_arg_1.to_csv(path_ukp_confvarg_v1_preprocessed,quotechar='"',sep=",",quoting=csv.QUOTE_ALL,encoding="utf-8",
                             columns=['argument-id','argument'],index=False)

    df_ukp_conv_arg_1=fuzzy_merge_topic_ids(df_ukp_conv_arg_1,df_topics)
    df_ukp_conv_arg_1.to_csv(path_argument_topic,sep=",",quotechar='"',quoting=csv.QUOTE_ALL,encoding="utf-8",
                             columns=['argument-id','topic-id'],index=False)
preprocess()