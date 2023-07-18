import pandas as pd
import os
from conf.configuration import *
import csv
import logging
from utils import *
def parse_file(path):
    with open(path) as argument_file:
        argument = " ".join(argument_file.readlines())
        return argument.strip()

def preprocess_corpus():

    topics = ['gayRights','marijuana','abortion','obama']
    path_source =get_path_source('utdallas-ideological-debates-reasons')
    path_preprocessed= get_path_preprocessed_arguments('utdallas-ideological-debates-reasons')
    path_argument_topic=get_path_argument_topic('utdallas-ideological-debates-reasons')
    path_topics = get_path_preprocessed_topics('utdallas-ideological-debates-reasons')
    df_topics = pd.read_csv(path_topics,sep=",",encoding="utf-8")

    arguments=[]
    ids=[]
    arguments_topics=[]
    for topic in topics:
        logging.warning("preprocessing %s"%topic)
        for root,dirs,files in os.walk(path_source+'/'+topic):
            for file in files:
                if file.endswith("data"):
                    path_file =os.path.join(root,file)
                    logging.warning("parsing %s"%path_file)
                    argument=parse_file(path_file)
                    logging.warning("getting %s"%argument)
                    arguments.append(argument)
                    file_id = file.replace(".data",'')
                    ids.append(topic+"-"+file_id)
                    if topic =='gayRights':
                        arguments_topics.append('gay marriage')
                    else:
                        arguments_topics.append(topic)

    df_arguments = pd.DataFrame({'argument-id':ids,'argument':arguments,'topic':arguments_topics})
    df_arguments['argument']=df_arguments.apply((lambda row: drop_separator(row['argument'],"\",\"")),axis=1)
    df_arguments.to_csv(path_preprocessed,quotechar='"',sep=",",quoting=csv.QUOTE_ALL,encoding="utf-8", \
                        columns=['argument-id','argument'],index=False)

    df_arguments=df_arguments.merge(df_topics,on="topic")
    df_arguments.to_csv(path_argument_topic,quotechar='"',sep=",",quoting=csv.QUOTE_ALL,encoding="utf-8", \
                        columns=['argument-id','topic-id'],index=False)
preprocess_corpus()