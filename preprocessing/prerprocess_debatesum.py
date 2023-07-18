import pandas as pd
from conf.configuration import *
from preprocessing.utils import *
from mylogging.mylogging import *
import csv
from tqdm import tqdm

def preprocess_corpus():
    path_source=get_path_source('debatesum')
    path_preprocessed_documents=get_path_preprocessed_documents('debatesum')
    df=pd.read_csv(path_source)
    df['document']=df['Full-Document']
    df['document-id']=range(0,df.shape[0])
    clean_documents(df)
    save_documents(df, path_preprocessed_documents)



setup_logging('../logs/preprocess-debatesum.log')
preprocess_corpus()