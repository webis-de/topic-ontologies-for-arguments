import pandas as pd

from conf.configuration import *
import csv
from topic_modeling.topics import *

def create_topics_dataframe_columns():
    columns={'id':[],
             'name':[],
             'url':[],
             'description':[],
             'ontology':[],
             'parent':[]
             }
    return columns


def save_topics():
    path_wikipedia= get_path_source('ontology-debatepedia')
    df_debatepedia = pd.read_csv(path_wikipedia).sort_values('concept')
    columns = create_topics_dataframe_columns()
    topic_index = 0
    for index,row in df_debatepedia.iterrows():
        columns['name'].append(row['concept'])
        columns['parent'].append("")
        columns['description'].append("")
        topic_for_url= row['concept'].replace(" ","_")
        columns['url'].append("http://debatepedia.idebate.org/en/index.php/Category:%s"%topic_for_url)
        columns['id'].append("2.%d"%topic_index)
        topic_index = topic_index+ 1
    columns['ontology']= ["debatepedia" for topic in columns['name']]
    topics_df  = pd.DataFrame(columns)
    topics_df.set_index('id')
    path_topics= get_path_topics('ontology-debatepedia')
    topics_df.to_csv(path_topics,sep=",",quoting=csv.QUOTE_ALL,quotechar='"',encoding='utf-8',index=False)

save_topics()