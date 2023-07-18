import csv
import json
import pandas as pd
from conf.configuration import *
from utils import *

def preprocess():
    path_source_cornell_erulemaking = get_path_source('cornell-erulemaking')
    path_preprocessed_cornell_erulemaking = get_path_preprocessed_documents('cornell-erulemaking')
    print(path_source_cornell_erulemaking)
    documents = []
    document_ids = []
    with open(path_source_cornell_erulemaking,'r') as file_cornell_erulemaking:
        for comment in file_cornell_erulemaking:
            comment_json_object= json.loads(comment)
            document_ids.append(comment_json_object['commentID'])
            comment_text=""
            for preprosition in comment_json_object['propositions']:
                comment_text=comment_text+" "+ preprosition['text']
            documents.append(comment_text)
    dataframe_cornell_erulemaking = pd.DataFrame({'document-id':document_ids,'document':documents})
    dataframe_cornell_erulemaking['document']=dataframe_cornell_erulemaking.apply((lambda row: drop_separator(row['document'],"\",\"")),axis=1)
    dataframe_cornell_erulemaking.to_csv(path_preprocessed_cornell_erulemaking,quotechar='"',sep=",",quoting=csv.QUOTE_ALL, \
                                         columns=['document-id','document'],encoding="utf-8",index=False)

preprocess()