import json
from conf.configuration import *
import pandas as pd
from preprocessing.utils import *
from mylogging.mylogging import *
import csv
from tqdm import tqdm
def extract_clause(argument,clauses,case_text,clause_id_to_extract):
    log(f"extracting {clause_id_to_extract}")
    for clause in clauses:
        if clause['_id']==clause_id_to_extract:
            clause_start=clause['start']
            clause_end=clause['end']
            clause=case_text[clause_start:clause_end]
            log(f"extracted {clause}")
            return clause

    raise ValueError(f"{clause_id_to_extract} not found!")

def extract_premises(argument,clauses,case_text):
    premises=""
    counter=0
    for clause_id in argument['premises']:

        clause=extract_clause(argument,clauses,case_text,clause_id)

        if counter == 0:
            premises= premises + clause
        else:
            premises = premises + " " + clause
        counter=counter + 1
    return premises

def extract_conclusion(argument,clause_ids,clause_text):
    return extract_clause(argument,clause_ids,clause_text,argument['conclusion'])

def preprocess_corpus():
    argument_texts=[]
    argument_ids=[]
    path_source=get_path_source('echr')
    path_preprocessed_documents =get_path_preprocessed_documents('echr')

    with open(path_source) as json_file:
        corpus=json.load(json_file)
        log(f"opened {path_source}")
        argument_id=0
        for case_id,case in tqdm(enumerate(corpus)):
            log_status(case_id,len(corpus),True)
            arguments = case['arguments']
            case_text = case['text']
            clauses= case['clauses']

            for argument in arguments:
                premises = extract_premises(argument,clauses,case_text)
                conclusion = extract_conclusion(argument,clauses,case_text)
                argument_text = conclusion + " " + premises
                argument_texts.append(argument_text)
                argument_ids.append(argument_id)
                argument_id=argument_id + 1
        df_documents=pd.DataFrame({'document':argument_texts,'document-id':argument_ids})
        df_documents=clean_documents(df_documents)
        log_size('echr',df_documents.shape[0])
        log(f"saving to {path_preprocessed_documents}")

        save_documents(df_documents,path_preprocessed_documents)


setup_logging('../logs/preprocess-echr.log')
preprocess_corpus()