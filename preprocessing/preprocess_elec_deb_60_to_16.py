import pandas as pd
import csv
from conf.configuration import *
import os
from utils import *
def read_file_path(path):
    with open(path) as file:
        lines =list(map(lambda line: line.replace('\n','').replace('\t',''),file.readlines()))
        return "".join(lines)
def preprocess():
    path_elec_deb_60_16 =get_path_source('elec-deb-60-to-16')
    documents = []
    for root,dirs,files in os.walk(path_elec_deb_60_16):
        for file in files:
            if file.endswith("txt"):
                file_path = os.path.join(root,file)
                document= read_file_path(file_path)
                documents.append(document)
    ids= list(map(lambda name: name.replace(".txt",""),filter(lambda name: name.endswith('txt'),files)))
    path_elec_deb_60_16_preprocessed_documents = get_path_preprocessed_documents('elec-deb-60-to-16')
    dataframe_election_debate= pd.DataFrame({"document-id":ids,'document':documents})
    dataframe_election_debate['document']=dataframe_election_debate.apply((lambda row: drop_separator(row['document'],"\",\"")),axis=1)
    dataframe_election_debate.to_csv(path_elec_deb_60_16_preprocessed_documents,quotechar='"',sep=",",quoting=csv.QUOTE_ALL, \
                                     columns=['document-id','document'],encoding="utf-8",index=False)
preprocess()