import pandas as pd
from conf.configuration import *
import csv
from utils import *
def preprocess_corpus():
    justification_label='Justification:'
    scores_label='Scores'
    assertion_label="Assertion:"
    persuasiveness_label='Persuasiveness:'
    instance_id_label='Instance ID:'
    path_source = get_path_source('utdallas-idebate-persuasiveness')
    path_prerocessed_arguments = get_path_preprocessed_arguments('utdallas-idebate-persuasiveness')
    assertion_label_read=False
    scores_label_read=False
    arguments=[]
    argument_ids=[]
    persuasiveness_values=[]
    justification=None
    with open(path_source,'r') as corpus_file:
        for line in corpus_file:
            line = line.strip()
            if line == assertion_label:
                assertion_label_read=True
                justification=""
            elif line.startswith(scores_label):
                arguments.append(justification)
                assertion_label_read=False
                scores_label_read=True
            elif assertion_label_read:
                if line == justification_label:
                    continue
                if len(line)==0:
                    continue
                if line.startswith('['):
                    continue
                justification= justification+ line.strip().replace("\n","")
            elif scores_label_read:
                persuasiveness_value_index = line.find(persuasiveness_label)+len(persuasiveness_label)
                value=line[persuasiveness_value_index:persuasiveness_value_index+1]
                persuasiveness_values.append(value)
                scores_label_read=False
            elif line.startswith(instance_id_label):
                id = line[len(instance_id_label)+1:]
                id=id.strip().replace('\n','')
                argument_ids.append(id)
            else:
                continue


    print("size of argument ids is %d"%len(argument_ids))
    print("size of arguments is %d"%len(arguments))
    print("size of persuasiveness values is %d"%len(persuasiveness_values))
    df_idebate_persuasiveness = pd.DataFrame({"argument-id":argument_ids,"argument":arguments})
    df_idebate_persuasiveness ['argument']=df_idebate_persuasiveness .apply((lambda row: drop_separator(row['argument'],"\",\"")),axis=1)
    df_idebate_persuasiveness.to_csv(path_prerocessed_arguments,quotechar='"',sep=",",quoting=csv.QUOTE_ALL,encoding="utf-8",index=False)


preprocess_corpus()