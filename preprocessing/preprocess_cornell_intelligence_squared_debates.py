import json
import pandas as pd
from conf.configuration import *
import csv
from utils import *
def preprocess_corpus():
    path_preprocessed_documents = get_path_preprocessed_documents("cornell-intelligence-squared-debates")
    path_source = get_path_source("cornell-intelligence-squared-debates")
    ids = []
    documents = []
    with open(path_source, "r") as f:
        debates = json.load(f)
        for debate in debates:
            ids.append(debate)
            document=""
            for transcript in debates[debate]['transcript']:
                text = " ".join(transcript['paragraphs'])
                document = document + text
            document=document.replace("\t","").replace("\n","")
            documents.append(document)
    df= pd.DataFrame({'document-id':ids,'document':documents})
    df['document']=df.apply((lambda row: drop_separator(row['document'],"\",\"")),axis=1)
    df.to_csv(path_preprocessed_documents,quotechar='"',sep=",",quoting=csv.QUOTE_ALL,encoding="utf-8", \
              columns=['document-id','document'],index=False)
    print(path_source)

preprocess_corpus()