import pandas as pd
from conf.configuration import *
import csv
from utils import *

def preprocess():
    path_preprocessed_arguments = get_path_preprocessed_arguments('ukp-ukpsentential')
    path_ukp_sentential_source = get_path_source('ukp-ukpsentential')
    path_argument_topic=get_path_argument_topic('ukp-ukpsentential')
    df_sentential=pd.read_csv(path_ukp_sentential_source,sep=",",encoding="utf-8",)
    path_preprocessed_topics = get_path_preprocessed_topics('ukp-ukpsentential')

    df_preprocessed_topics = pd.read_csv(path_preprocessed_topics,sep=",",encoding="utf-8",quotechar="\"")
    df_sentential=df_sentential.merge(df_preprocessed_topics ,on='topic')
    df_sentential= df_sentential[['sentence','topic-id']]
    df_sentential.rename(columns={'sentence':'argument'},inplace=True)
    df_sentential['argument-id']=range(0,df_sentential.shape[0])
    df_sentential.to_csv(path_preprocessed_arguments,sep=",",quoting=csv.QUOTE_ALL,encoding="utf-8",
                         columns=['argument-id','argument'],index=False)
    df_sentential['argument']=df_sentential.apply((lambda row: drop_separator(row['argument'],"\",\"")),axis=1)
    df_sentential.to_csv(path_argument_topic,sep=",",quoting=csv.QUOTE_ALL,encoding="utf-8",
                         columns=['argument-id','topic-id'],index=False)

preprocess()