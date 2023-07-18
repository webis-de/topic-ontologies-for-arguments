from conf.configuration import *
import pandas as pd
import csv
import os
from utils import *
import re
def load_topics():
    path_preprocessed_topics = get_path_preprocessed_topics("ukp-ukpconvarg-v2")
    df_topics=pd.read_csv(path_preprocessed_topics,sep=",",encoding="utf-8")
    df_topics['topic']=df_topics.apply(lambda topic:topic['topic'].lower().replace("?",'').replace("-"," "),axis=1)
    df_topics['topic']=df_topics.apply(lambda topic:re.sub(r"\s+"," ",topic['topic']),axis=1)
    return df_topics

def extract_topic(filename):
    _index=filename.index("_")
    topic=filename[:_index]
    topic=topic.replace("-",' ')
    return topic

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

def parse_debate(file_path):
    arguments=[]
    debate_dataframe= pd.read_csv(file_path,sep="\t",encoding="utf-8",header=None)
    try:
        debate_arguments_1 = list(debate_dataframe.iloc[:,2])
        debate_arguments_2 = list(debate_dataframe.iloc[:,3])
        paired_argument_ids = list(debate_dataframe.iloc[:,0])
        argument_ids = parse_argument_ids(paired_argument_ids)
    except IndexError:
        print(file_path)

    arguments.extend(debate_arguments_1)
    arguments.extend(debate_arguments_2)
    print(file_path.split("/")[-1])
    print(len(arguments))
    return arguments, argument_ids

def preprocess():
    path_ukp_convarg_v2 = get_path_source("ukp-ukpconvarg-v2")
    path_ukp_confvarg_v2_preprocessed = get_path_preprocessed_arguments("ukp-ukpconvarg-v2")
    path_argument_topic=get_path_argument_topic('ukp-ukpconvarg-v2')
    df_topics=load_topics()

    all_argument_ids=[]
    all_arguments=[]
    topics=[]

    for root,dirs,files in os.walk(path_ukp_convarg_v2):
        for file_name in sorted(files):
            topic=extract_topic(file_name)

            file_path = os.path.join(root,file_name)
            arguments,argument_ids= parse_debate(file_path)
            all_arguments.extend(arguments)
            all_argument_ids.extend(argument_ids)
            topics.extend([topic for _ in arguments])

    df_ukp_conv_arg_2 = pd.DataFrame({"argument-id":all_argument_ids,"argument":all_arguments,"topic":topics})
    df_ukp_conv_arg_2['argument']=df_ukp_conv_arg_2.apply((lambda row: drop_separator(row['argument'],"\",\"")),axis=1)
    df_ukp_conv_arg_2.to_csv(path_ukp_confvarg_v2_preprocessed,quotechar='"',sep=",",quoting=csv.QUOTE_ALL,encoding="utf-8",
                             columns=['argument-id','argument'],index=False)
    df_ukp_conv_arg_2=fuzzy_merge_topic_ids(df_ukp_conv_arg_2,df_topics)
    df_ukp_conv_arg_2['argument']=df_ukp_conv_arg_2.apply((lambda row: drop_separator(row['argument'],"\",\"")),axis=1)
    df_ukp_conv_arg_2.to_csv(path_argument_topic,quotechar='"',sep=",",quoting=csv.QUOTE_ALL,encoding="utf-8",
                             columns=['argument-id','topic-id'],index=False)
preprocess()