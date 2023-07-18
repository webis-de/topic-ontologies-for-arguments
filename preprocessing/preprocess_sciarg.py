import os
import re
import pandas as pd
from utils import *
from conf.configuration import *
from gatenlp import Document
def preprocess_corpus():
    path_source = get_path_source('sci-arg')
    path_preprocessed_documents = get_path_preprocessed_documents('sci-arg')
    path_document_topics= get_path_document_topic('sci-arg')
    documents=[]
    file_names = sorted(os.listdir(path_source))
    cleaned_files = [file.replace(".txt","") for file in file_names]
    topic_ids=[0 for file in cleaned_files]

    for file_name in file_names:
        path_file=os.path.join(path_source,file_name)
        doc = Document.load(path_file)

        documents.append(doc.text)


    df_documents=pd.DataFrame({'document-id':cleaned_files,'document':documents,'topic-id':topic_ids})
    df_documents=clean_documents(df_documents)
    df_documents.to_csv(path_preprocessed_documents,sep=",",quotechar='"',quoting=csv.QUOTE_ALL,encoding="utf-8",columns=['document-id','document'],index=False)
    df_documents.to_csv(path_document_topics,sep=",",quotechar='"',quoting=csv.QUOTE_ALL,encoding="utf-8",columns=['document-id','topic-id'],index=False)

preprocess_corpus()