import pandas as pd
import json
from conf.configuration import *
import tqdm
import csv
from utils import drop_separator

def entry2argument(entry):
    if 'sourceId' in entry['context']:
        debate_id = entry['context']['sourceId']
    else:
        debate_id = entry['context']['source.id']

    if 'discussionTitle' in entry['context']:
        topic = entry['context']['discussionTitle'].lower()
    else:
        topic = entry['context']['source.title'].lower()

    conclusion = entry['conclusion'].lower()
    premise = entry['premises'][0]['text'].lower()
    argument_id = entry['id']

    return (debate_id,argument_id,conclusion,premise,topic)

def preprocess():

    dataset_source_path = get_path_source('args-me')
    dataset_preprocessed_path =get_path_preprocessed_arguments('args-me')
    document_ids=[]
    argument_ids=[]
    texts=[]
    topics=[]

    with open(dataset_source_path) as json_file:
        data = json.load(json_file)
        for entry in tqdm.tqdm(data['arguments']):

            debate_id,argument_id,conclusion,premise,topic = entry2argument(entry)
            document_ids.append(debate_id)
            argument_ids.append(argument_id)
            text = conclusion +" "+ premise
            texts.append(text)
            topics.append(topic)
        preprocessed_data_frame= pd.DataFrame({"argument":texts,"topic":topics,"argument-id":argument_ids,"document-id":document_ids,"topic":topics})
        preprocessed_data_frame['argument']=preprocessed_data_frame.apply((lambda row: drop_separator(row['argument'],"\",\"")),axis=1)
        preprocessed_data_frame.to_csv(dataset_preprocessed_path,quotechar='"',sep=",",quoting=csv.QUOTE_ALL,encoding="utf-8", \
                                       index=False,columns=['argument-id','argument'])
    print("finished preprocessing")

preprocess()