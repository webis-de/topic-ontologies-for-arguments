import pandas as pd
import json
from conf.configuration import *
import csv
import logging
logging.basicConfig(filename='../logs/preprocess-change-my-view.log')
from utils import *

def prase_argumens(path):
    arguments=[]
    argument_ids=[]
    with open(path,'r') as json_file:
        for line in json_file:
            data = json.loads(line)


            for comment in data['positive']['comments']:
                if data['op_name'] not in argument_ids:
                    argument_ids.append(data['op_name'])
                    arguments.append(data['op_text'].strip().replace('\n',' ').replace('\t',' ').replace("\""," "))
                if comment['name'] not in argument_ids:
                    arguments.append(comment['body'].strip().replace('\n',' ').replace('\t',' ').replace("\""," "))
                    argument_ids.append(comment['name'])

            for comment in data['negative']['comments']:
                if data['op_name'] not in argument_ids:
                    argument_ids.append(data['op_name'])
                    arguments.append(data['op_text'].strip().replace('\n',' ').replace('\t',' ').replace("\""," "))
                if comment['name'] not in argument_ids:
                    arguments.append(comment['body'].strip().replace('\n',' ').replace('\t',' ').replace("\""," "))
                    argument_ids.append(comment['name'])

    return arguments,argument_ids
def preprocess():

    dataset_source_train_path = get_path_source_part('cornell-change-my-view', 'training')
    print(dataset_source_train_path)
    dataset_source_heldout_path = get_path_source_part('cornell-change-my-view', 'heldout')
    print(dataset_source_heldout_path)
    dataset_preprocessed_path = get_path_preprocessed_arguments('cornell-change-my-view')
    t_arguments,t_argument_ids= prase_argumens(dataset_source_train_path)
    h_arguments,h_argument_ids= prase_argumens(dataset_source_heldout_path)
    t_arguments.extend(h_arguments)
    t_argument_ids.extend(h_argument_ids)
    preprocessed_data_frame= pd.DataFrame({"argument":t_arguments,"argument-id":t_argument_ids})
    preprocessed_data_frame['argument-striped']=preprocessed_data_frame.apply(lambda row:row['argument'].strip(),axis=1)
    del preprocessed_data_frame['argument']
    empty_arguments= preprocessed_data_frame[preprocessed_data_frame['argument-striped']==""]
    logging.warning("found %d empty arguments"%empty_arguments.shape[0])
    preprocessed_data_frame=preprocessed_data_frame[preprocessed_data_frame['argument-striped']!=""]
    preprocessed_data_frame.rename(columns={'argument-striped':'argument'},inplace=True)
    preprocessed_data_frame['argument']=preprocessed_data_frame.apply((lambda row: drop_separator(row['argument'],"\",\"")),axis=1)
    preprocessed_data_frame.to_csv(dataset_preprocessed_path,quotechar='"',sep=",",quoting=csv.QUOTE_ALL,encoding="utf-8",columns=['argument-id','argument'],index=False)


preprocess()