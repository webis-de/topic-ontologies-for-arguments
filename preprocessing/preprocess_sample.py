import pandas as pd
from conf.configuration import *
import csv



def preprocess():
    path=get_path_source('sample')
    path_preprocessed= get_path_preprocessed_documents('sample')
    df_original_arguments= pd.read_csv(path,quotechar='"',sep=",",quoting=csv.QUOTE_ALL,encoding='utf-8')
    df_original_arguments.to_csv(path_preprocessed,quotechar='"',sep=",",quoting=csv.QUOTE_ALL,encoding="utf-8",index=False)
    print(path)
    print(path_preprocessed)


def remove_duplicates():
    path_preprocessed_duplicates= get_path_preprocessed_documents_version('sample','duplicates')
    path_preprocessed= get_path_preprocessed_documents('sample')
    df_original_arguments= pd.read_csv(path_preprocessed_duplicates,quotechar='"',sep=",",quoting=csv.QUOTE_ALL,encoding='utf-8',index_col='document-id')
    df_original_arguments_duplicated=df_original_arguments[df_original_arguments['corpus']=='utdallas-icle-essay-scoring']
    df_original_arguments_duplicates =df_original_arguments_duplicated.sample(n=5)
    df_original_arguments_no_duplicates = df_original_arguments[~df_original_arguments.isin(df_original_arguments_duplicates).all(1)]
    df_original_arguments_no_duplicates.to_csv(path_preprocessed,quotechar='"',sep=",",quoting=csv.QUOTE_ALL,encoding="utf-8")
#preprocess()

remove_duplicates()