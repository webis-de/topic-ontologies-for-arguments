import pandas as pd

from conf.configuration import *
import csv

def create_topics_dataframe_columns():
    columns={'id':[],
          'name':[],
          'url':[],
          'description':[],
          'ontology':[],
          'parent':[]
          }
    return columns

def save_global_issues():
    path_global_issues= '/mnt/ceph/storage/data-in-progress/args-topic-modeling/corpora/strategic-intelligence/global-issues.csv'
    path_topics= get_path_topics('ontology-strategic-intelligence')
    df_global_issues =pd.read_csv(path_global_issues).sort_values('global_issue.title')
    columns = create_topics_dataframe_columns()
    columns['name']=df_global_issues['global_issue.title']
    columns['url']=df_global_issues['global_issue.url']
    columns['description']=df_global_issues['global_issue.summary']
    columns['ontology']= ["strategic-intelligence" for topic in columns['name']]
    columns['id'] = [format_global_issue_id(id) for id in range(len(columns['name']))]
    columns['parent'] = ["" for topic in columns['name']]
    topics_df  = pd.DataFrame(columns)
    topics_df.set_index('id')
    topics_df.to_csv(path_topics,sep=",",quoting=csv.QUOTE_ALL,quotechar='"',encoding='utf-8',index=False)

def save_local_issues():
    path_local_issues = '/mnt/ceph/storage/data-in-progress/args-topic-modeling/corpora/strategic-intelligence/key-issues-final.csv'
    path_topics= get_path_topics('ontology-strategic-intelligence-sub-topics')
    path_global_topics=get_path_topics('ontology-strategic-intelligence')
    df_global_topics =pd.read_csv(path_global_topics,sep=",",quoting=csv.QUOTE_ALL,quotechar='"',encoding="utf-8",dtype={'id': object})
    df_local_issues = pd.read_csv(path_local_issues,sep=",",quoting=csv.QUOTE_ALL,quotechar='"',encoding="utf-8").sort_values(['key_issue.title'])
    columns = create_topics_dataframe_columns()
    columns['name']=df_local_issues['key_issue.title']
    columns['description']=df_local_issues['key_issue.summary']
    columns['ontology']= ["strategic-intelligence-sub-topics" for topic in columns['name']]
    columns['url']=["" for topic in columns['name']]
    local_issue_id=0
    for global_topic in list(df_local_issues['global_issue.title']):
        if global_topic.startswith('[') and global_topic.endswith(']'):
            multiple_global_topics = [one_topic.strip("'") for one_topic in global_topic.strip("[]").split("', ")]
            multiple_parents= []
            columns['parent'].append(multiple_parents)
            for sparate_global_topic in multiple_global_topics :
                global_issue_id=df_global_topics.loc[df_global_topics['name']==sparate_global_topic,'id'].values[0]
                multiple_parents.append(global_issue_id)
        else:
            global_issue_id=df_global_topics.loc[df_global_topics['name']==global_topic,'id'].values[0]
            print(global_issue_id)
            columns['parent'].append(global_issue_id)
        columns['id'].append(format_local_issue_id(local_issue_id))
        local_issue_id=local_issue_id+1
    topics_df  = pd.DataFrame(columns)
    topics_df.to_csv(path_topics,sep=",",quoting=csv.QUOTE_ALL,quotechar='"',encoding='utf-8',index=False)

def format_global_issue_id(global_issue_id):
    global_issue_id_formatted= "1.{0}".format(int(global_issue_id))
    return global_issue_id_formatted

def format_local_issue_id(local_issue_id):
    local_issue_id_formatted= "4.{0}".format(int(local_issue_id))
    return local_issue_id_formatted




save_global_issues()
save_local_issues()