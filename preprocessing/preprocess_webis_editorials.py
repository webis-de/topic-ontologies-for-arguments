import pandas as pd
from conf.configuration import *
import csv
from utils import *
def prase_file(path):
    file = open(path,'r',encoding="utf8", errors='ignore')
    segments = []
    ids = []
    labels = []
    for line in file:
        tokens = line.split("\t")
        id = tokens[0]
        if len(tokens)> 1:
            segment_label = tokens[1]
        else:
            segment_label = "None"
        if len(tokens)> 2:
            segment = tokens[2].strip()
        else:
            segment=""
        segments.append(segment)
        ids.append(id)
        labels.append(segment_label)
    return ids,labels,segments

def dump_file():
    for root,directories,files in os.walk(corpus_root_path):
        for file_name in files:
            file_path = os.path.join(root,file_name)
            ids,labels,segments= prase_file(file_path)
            document = " ".join(segments)
def preprocess():
    corpus_root_path = get_path_source_part("webis-editorials-16", "documents")
    preprocessed_documents_path = get_path_preprocessed_documents("webis-editorials-16")
    documents = []
    document_ids = []

    for root,directories,files in os.walk(corpus_root_path):
        for file_name in files:
            file_path = os.path.join(root,file_name)
            ids,labels,segments= prase_file(file_path)
            document = " ".join(segments)
            if len(document)==0:
                continue
            documents.append(document)
            document_ids.append(file_name)
    editorials_df= pd.DataFrame({"document":documents,"document-id":document_ids})
    editorials_df['document']=editorials_df.apply((lambda row: drop_separator(row['document'],"\",\"")),axis=1)
    editorials_df.info()
    editorials_df.to_csv(preprocessed_documents_path,quotechar='"',sep=",",quoting=csv.QUOTE_ALL,encoding="utf-8", \
                         columns=["document-id","document"],index=False)

preprocess()