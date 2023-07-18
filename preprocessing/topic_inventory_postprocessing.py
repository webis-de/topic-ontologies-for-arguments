import pandas as pd
from conf.configuration import *
from datetime import datetime
import logging
import csv
def setup_logging_duplicates():
    logging.basicConfig(filename="../logs/topic-inventory-duplicates.log",format="%(message)s")

def setup_logging_new_ids():
    logging.basicConfig(filename="../logs/topic-inventory-new-ids.log",format="%(message)s")

def load_duplicate_topics():
    duplicate_topics= {}
    duplicate_topics[304]=196
    duplicate_topics[268]=176
    duplicate_topics[471]=144
    duplicate_topics[296]=154
    duplicate_topics[490]=323
    duplicate_topics[536]=245
    return duplicate_topics

def fix_naming_error():
    path_duplicated_preprocessed_topics=get_path_preprocessed_part('topic-inventory','corpora-topics-duplicates')
    path_preprocessed_topics=get_path_preprocessed_part('topic-inventory','corpora-topics')

    df_topics=pd.read_csv(path_duplicated_preprocessed_topics,sep=",",encoding="utf-8",dtype={'new-id':int})
    df_preprocessed_topics=load_preprocessed_topic_inventory()
    df_errors_topic=df_topics[~df_topics['error'].isna()]
    df_errors_topic=df_errors_topic[['new-id','topic']]
    logging.warning("updating %d duplicated_topics"%df_errors_topic.shape[0])
    df_errors_topic.rename(columns={'new-id':'id','topic':'new-topic'},inplace=True)
    df_preprocessed_topics=df_preprocessed_topics.merge(df_errors_topic,on='id',how='left')
    df_preprocessed_topics['topic']=df_preprocessed_topics.apply(lambda record:record['new-topic'] if (isinstance(record['new-topic'],str) and len(record['new-topic'])>0) else record['topic'],axis=1)
    logging.warning("saving the preprocessed topics to %s"%path_preprocessed_topics)
    df_preprocessed_topics.to_csv(path_preprocessed_topics,sep=",",encoding="utf-8",index=False,columns=['topic','id','error'])

def update_duplicated_topics_in_preprocessed_topic_inventory():
    path_duplicated_preprocessed_topics=get_path_preprocessed_part('topic-inventory','corpora-topics-duplicates')
    path_preprocessed_topics=get_path_preprocessed_part('topic-inventory','corpora-topics')

    df_topics=pd.read_csv(path_duplicated_preprocessed_topics,sep=",",encoding="utf-8",dtype={'new-id':int})
    df_preprocessed_topics=load_preprocessed_topic_inventory()

    df_duplicate_topics=df_topics[~df_topics['unique-id'].isna()]

    duplicated_topics=df_duplicate_topics['unique-id'].astype(int).values
    df_duplicated_topics=df_topics[df_topics['new-id'].isin(duplicated_topics)]
    df_duplicated_topics=df_duplicated_topics[['new-id','topic']]
    df_duplicated_topics.rename(columns={'new-id':'id','topic':'new-topic'},inplace=True)
    df_duplicated_topics.info()
    logging.warning("updating %d duplicated_topics"%df_duplicated_topics.shape[0])


    df_preprocessed_topics=df_preprocessed_topics.merge(df_duplicated_topics,on='id',how='left')
    df_preprocessed_topics.sort_values('id',inplace=True)
    df_preprocessed_topics['topic']=df_preprocessed_topics.apply(lambda record:record['new-topic'] if (isinstance(record['new-topic'],str) and len(record['new-topic'])>0) else record['topic'],axis=1)
    path_preprocessed_topics=path_preprocessed_topics.replace(".csv",".debug.csv")
    logging.warning("saving the preprocessed topics to %s"%path_preprocessed_topics)
    df_preprocessed_topics.to_csv(path_preprocessed_topics,sep=",",encoding="utf-8",index=False,columns=['topic','id','error'])

def load_duplicate_topics_2():
    path_preprocessed_topics=get_path_preprocessed_part('topic-inventory','corpora-topics-duplicates')
    df_topics=pd.read_csv(path_preprocessed_topics,sep=",",encoding="utf-8",dtype={'new-id':int})
    df_duplicate_topics=df_topics[~df_topics['unique-id'].isna()]
    duplicate_topics={}
    def add_duplicate_topic(record):

        duplicate_topics[int(record['new-id'])]=int(record['unique-id'])
        logging.warning("matching %d with %d"%(int(record['new-id']),int(record['unique-id'])))

    df_duplicate_topics.apply(add_duplicate_topic,axis=1)
    logging.warning("dropping %d duplicates"%len(duplicate_topics))
    return duplicate_topics
def load_preprocessed_topic_inventory():
    path_preprocessed_topics=get_path_preprocessed_part('topic-inventory','corpora-topics')
    df_preprocessed_topics = pd.read_csv(path_preprocessed_topics,sep=",",encoding="utf-8",dtype={'topic':str})
    return df_preprocessed_topics
def show_duplicate_topics(duplicate_topics):

    df_preprocessed_topics = load_preprocessed_topic_inventory()
    for topic_to_merge_id in duplicate_topics.keys():
        topic_id = duplicate_topics[topic_to_merge_id]
        topic_to_merge=df_preprocessed_topics[df_preprocessed_topics['id']==topic_to_merge_id].topic.iloc[0]
        topic = df_preprocessed_topics[df_preprocessed_topics['id']==topic_id].topic.iloc[0]
        logging.warning(topic_to_merge+ " --> " + topic)

def drop_duplicate_topics_from_preprocessed_topic_inventory(duplicate_topics):
    path_preprocessed_topics=get_path_preprocessed_part('topic-inventory','corpora-topics')
    df_preprocessed_topics = pd.read_csv(path_preprocessed_topics,sep=",",encoding="utf-8",dtype={'topic':str})
    logging.warning("size of preprocessed topics before dropping %d" %df_preprocessed_topics.shape[0])
    df_preprocessed_topics=df_preprocessed_topics[~df_preprocessed_topics['id'].isin(duplicate_topics.keys())]
    logging.warning("size of preprocessed topics after dropping %d" %df_preprocessed_topics.shape[0])
    #path_preprocessed_topics=path_preprocessed_topics.replace(".csv",".debug.csv")
    logging.warning("saving updated into %s"%path_preprocessed_topics)
    df_preprocessed_topics.to_csv(path_preprocessed_topics,sep=",",encoding="utf-8",index=False)

def update_duplicate_topics_in_topic_inventory(duplicate_topics):
    path_topic_inventory_source=get_path_source_part('topic-inventory', 'corpora-topics')
    df_topic_inventory_source= pd.read_csv(path_topic_inventory_source,sep=",",encoding="utf-8")
    for index, corpus_topic_record in df_topic_inventory_source.iterrows():
        for topic_id_to_merge in duplicate_topics:
            if corpus_topic_record['id']==topic_id_to_merge:
                logging.warning("%d is matched"%topic_id_to_merge)
                topic_id=duplicate_topics[topic_id_to_merge]
                df_topic_inventory_source.loc[index,'id']=topic_id
    #path_topic_inventory_source=path_topic_inventory_source.replace(".csv",".debug.csv")
    logging.warning("saving updated into %s"%path_topic_inventory_source)
    df_topic_inventory_source.to_csv(path_topic_inventory_source,sep=",",encoding="utf-8",index=False)


def drop_duplicate_topics():
    setup_logging_duplicates()
    logging.warning(datetime.now())
    fix_naming_error()
    update_duplicated_topics_in_preprocessed_topic_inventory()
    duplicate_topics = load_duplicate_topics_2()
    drop_duplicate_topics_from_preprocessed_topic_inventory(duplicate_topics)
    update_duplicate_topics_in_topic_inventory(duplicate_topics)

def load_new_topic_id_map():
    path_preprocessed_topic_inventory_sorted=get_path_preprocessed_part('topic-inventory','corpora-topics-sorted')
    df_preprocessed_topic_inventory_sorted=pd.read_csv(path_preprocessed_topic_inventory_sorted,sep=",",encoding="utf-8",dtype={'id':int,'new-id':int})
    id_map={}
    for index,new_topic_id_record in df_preprocessed_topic_inventory_sorted.iterrows():
        new_id=new_topic_id_record['new-id']
        id=new_topic_id_record['id']
        id_map[id]=new_id
    return id_map
def update_topic_inventory_ids():
    setup_logging_new_ids()
    #update_preprocessed_topic_inventory_ids()
    #update_source_topic_inventory_ids()
    #update_preprocessed_topic_description_ids()
    update_preprocessed_topic_description_ids_candidates()
def update_preprocessed_topic_inventory_ids():
    id_map=load_new_topic_id_map()
    path_preprocessed_topic_inventory=get_path_preprocessed_part('topic-inventory','corpora-topics')
    path_preprocessed_topic_inventory_debug=path_preprocessed_topic_inventory.replace(".csv",".debug.csv")
    df_preprocessed_topic_inventory=pd.read_csv(path_preprocessed_topic_inventory,sep=",",encoding="utf-8")

    for index,preprocessed_topic_record in df_preprocessed_topic_inventory.iterrows():
        id =preprocessed_topic_record['id']
        new_id=id_map[id]
        logging.warning("changing topic id from %d to %d"%(id,new_id))
        df_preprocessed_topic_inventory.loc[index,'id']=new_id
    logging.warning("saving new preprocesed topic ids to %s  "%path_preprocessed_topic_inventory)
    df_preprocessed_topic_inventory.to_csv(path_preprocessed_topic_inventory,sep=",",encoding="utf-8",index=False)

def update_source_topic_inventory_ids():
    id_map=load_new_topic_id_map()
    path_source_topic_inventory=get_path_source_part('topic-inventory', 'corpora-topics')
    #path_source_topic_inventory_debug=path_source_topic_inventory.replace('.csv','.debug.csv')
    df_topic_inventory = pd.read_csv(path_source_topic_inventory,sep=",",encoding="utf-8")
    counter= 0
    for index,preprocessed_topic_record in df_topic_inventory.iterrows():
        id =preprocessed_topic_record['id']
        new_id=id_map[id]
        logging.warning("changing topic id from %d to %d"%(id,new_id))
        df_topic_inventory.loc[index,'id']=new_id
        counter = counter +1

    logging.warning("updated %d records in %s"%(counter,path_source_topic_inventory))
    df_topic_inventory.to_csv(path_source_topic_inventory,sep=",",encoding="utf-8",index=False)

def update_preprocessed_topic_inventory_ids():
    id_map=load_new_topic_id_map()
    path_preprocessed_topic_inventory=get_path_preprocessed_part('topic-inventory','corpora-topics')
    #path_preprocessed_topic_inventory_debug=path_preprocessed_topic_inventory.replace(".csv",".debug.csv")
    df_preprocessed_topic_inventory=pd.read_csv(path_preprocessed_topic_inventory,sep=",",encoding="utf-8")

    for index,preprocessed_topic_record in df_preprocessed_topic_inventory.iterrows():
        id =preprocessed_topic_record['id']
        new_id=id_map[id]
        logging.warning("changing topic id from %d to %d"%(id,new_id))
        df_preprocessed_topic_inventory.loc[index,'id']=new_id
    logging.warning("saving new preprocesed topic ids to %s  "%path_preprocessed_topic_inventory)
    df_preprocessed_topic_inventory.to_csv(path_preprocessed_topic_inventory,sep=",",encoding="utf-8",index=False)

def update_preprocessed_topic_description_ids():
    id_map=load_new_topic_id_map()
    path_preprocessed_topics_descriptions=get_path_preprocessed_part('topic-inventory','corpora-topics-description')
    path_preprocessed_topics_descriptions_debug=path_preprocessed_topics_descriptions.replace(".csv",".debug.csv")
    df_preprocessed_topics_descriptions=pd.read_csv(path_preprocessed_topics_descriptions,sep=",",encoding="utf-8",quoting=csv.QUOTE_ALL)

    for index,preprocessed_topic_description_record in df_preprocessed_topics_descriptions.iterrows():
        id =preprocessed_topic_description_record['id']
        new_id=id_map[id]
        logging.warning("changing topic id from %d to %d"%(id,new_id))
        df_preprocessed_topics_descriptions.loc[index,'id']=new_id

    logging.warning("saving new preprocesed topic ids to %s " %path_preprocessed_topics_descriptions)
    df_preprocessed_topics_descriptions.to_csv(path_preprocessed_topics_descriptions,sep=",",encoding="utf-8",index=False)

def update_preprocessed_topic_description_ids():
    id_map=load_new_topic_id_map()
    path_preprocessed_topics_descriptions=get_path_preprocessed_part('topic-inventory','corpora-topics-description')
    path_preprocessed_topics_descriptions_debug=path_preprocessed_topics_descriptions.replace(".csv",".debug.csv")
    df_preprocessed_topics_descriptions=pd.read_csv(path_preprocessed_topics_descriptions,sep=",",encoding="utf-8",quoting=csv.QUOTE_ALL)

    for index,preprocessed_topic_description_record in df_preprocessed_topics_descriptions.iterrows():
        id =preprocessed_topic_description_record['id']
        if id in id_map:
            new_id=id_map[id]
            logging.warning("changing topic id from %d to %d"%(id,new_id))
            df_preprocessed_topics_descriptions.loc[index,'id']=new_id

    logging.warning("saving new preprocesed topic ids to %s " %path_preprocessed_topics_descriptions)

    df_preprocessed_topics_descriptions.to_csv(path_preprocessed_topics_descriptions,sep=",",encoding="utf-8",index=False)

def update_preprocessed_topic_description_ids_candidates():
    id_map=load_new_topic_id_map()
    path_preprocessed_topics_descriptions_candidates=get_path_preprocessed_part('topic-inventory','corpora-topics-description-candidates')

    df_preprocessed_topics_descriptions=pd.read_csv(path_preprocessed_topics_descriptions_candidates,sep=",",encoding="utf-8",quoting=csv.QUOTE_ALL)

    for index,preprocessed_topic_description_record in df_preprocessed_topics_descriptions.iterrows():
        id =preprocessed_topic_description_record['id']
        new_id=id_map[id]
        logging.warning("changing topic id from %d to %d"%(id,new_id))
        df_preprocessed_topics_descriptions.loc[index,'id']=new_id

    logging.warning("saving new preprocesed topic ids to %s " %path_preprocessed_topics_descriptions_candidates)
    df_preprocessed_topics_descriptions.to_csv(path_preprocessed_topics_descriptions_candidates,sep=",",encoding="utf-8",index=False)

def update_preprocessed_topic_description_accumlative():
    path_preprocessed_topics_descriptions_candidates=get_path_preprocessed_part('topic-inventory','corpora-topics-description-candidates')
    path_topic_descriptions_annotated=get_path_preprocessed_part('topic-inventory','corpora-topics-description')

    df_preprocessed_topics_descriptions_candidates=pd.read_csv(path_preprocessed_topics_descriptions_candidates,sep=",",encoding="utf-8",quoting=csv.QUOTE_ALL)
    df_preprocessed_topics_descriptions=pd.read_csv(path_topic_descriptions_annotated,sep=",",encoding="utf-8",quoting=csv.QUOTE_ALL)
    df_preprocessed_topics_descriptions_candidates=df_preprocessed_topics_descriptions_candidates[~df_preprocessed_topics_descriptions_candidates['id'].isin(df_preprocessed_topics_descriptions['id'])]




    df_preprocessed_topics_descriptions_candidates.to_csv(path_preprocessed_topics_descriptions_candidates+"1",sep=",",encoding="utf-8",index=False,columns=['id','topic','description-candidate','suitable'])

def concatenate_topic_description():
    path_topic_descriptions_annotated=get_path_preprocessed_part('topic-inventory','corpora-topics-description')
    df_preprocessed_topics_descriptions=pd.read_csv(path_topic_descriptions_annotated,sep=",",encoding="utf-8",quoting=csv.QUOTE_ALL)
    path_preprocessed_topics_descriptions_candidates=get_path_preprocessed_part('topic-inventory','corpora-topics-description-candidates')+"1"
    df_preprocessed_topics_descriptions_candidates=pd.read_csv(path_preprocessed_topics_descriptions_candidates,sep=",",encoding="utf-8",quoting=csv.QUOTE_ALL)
    df_preprocessed_topics_descriptions= pd.concat([df_preprocessed_topics_descriptions, df_preprocessed_topics_descriptions_candidates])
    df_preprocessed_topics_descriptions.to_csv(path_topic_descriptions_annotated,sep=",",encoding="utf-8",index=False,columns=['id','topic','description-candidate','suitable'])

if __name__ == '__main__':
    #update_preprocessed_topic_description_accumlative()
    concatenate_topic_description()