import pandas as pd
from conf.configuration import *
import csv
def match_new_topics_with_preprocessed():
    path_new_topics_new=get_path_source_part('topic-inventory','corpora-topics-new-3')
    path_preprocessed_topics=get_path_preprocessed_part('topic-inventory','corpora-topics')
    df_corpora_topics_new = pd.read_csv(path_new_topics_new,sep=",",encoding="utf-8")
    df_preprocessed_topics=pd.read_csv(path_preprocessed_topics,sep=",",encoding="utf-8")
    df_corpora_topics_new['topic']=df_corpora_topics_new['manually-cleaned']
    df_corpora_topics_new=df_corpora_topics_new.merge(df_preprocessed_topics,on='topic',how='left')
    df_corpora_topics_new.to_csv(path_new_topics_new,sep=",",encoding="utf-8",quoting=csv.QUOTE_ALL,index=False)

