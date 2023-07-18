import pandas as pd
import csv
from conf.configuration import *
from preprocessing.utils import *
def preprocess_gaq():
    path_source=get_path_source('gaq')
    path_documents=get_path_preprocessed_documents('gaq')
    df=pd.read_csv(path_source)
    df['document']=df['text']
    df=clean_documents(df)
    df['document-id']=range(0,df.shape[0])
    save_documents(df,path_documents)
preprocess_gaq()