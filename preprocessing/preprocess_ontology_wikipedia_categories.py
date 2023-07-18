import pandas as pd

from conf.configuration import *
import csv
path_wikipedia= get_path_source('ontology-wikipedia-categories')
df_wikipedia = pd.read_csv(path_wikipedia).sort_values('concept')
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
    path_wikipedia_categories= get_path_source('ontology-wikipedia-categories')
    df_wikipedia_categories = pd.read_csv(path_wikipedia_categories,sep=",",quoting=csv.QUOTE_ALL,quotechar='"',encoding='utf-8').sort_values('concept')
    columns = create_topics_dataframe_columns()
    topic_index = 0
    for index,row in df_wikipedia_categories.iterrows():
        columns['name'].append(row['concept'])
        columns['parent'].append("")
        columns['description'].append("")
        columns['url'].append("")
        columns['id'].append("5.%d"%topic_index)
        topic_index = topic_index+ 1
    columns['ontology']= ["wikipedia-categories" for topic in columns['name']]
    topics_df  = pd.DataFrame(columns)
    topics_df.set_index('id')
    path_topics= get_path_topics('ontology-wikipedia-categories')
    topics_df.to_csv(path_topics,sep=",",quoting=csv.QUOTE_ALL,quotechar='"',encoding='utf-8',index=False)

save_topics()