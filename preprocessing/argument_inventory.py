import pandas as pd
import json
from conf.configuration import *
import tqdm
import csv
import numpy as np
import logging
from preprocessing.utils import drop_separator
from datetime import datetime
from tqdm import tqdm
def setup_logging(filename):
    logging.basicConfig(filename=filename,level=logging.DEBUG,format="%(message)s")
    logging.warning(datetime.now())

def log_debug(message,debug):
    if debug:
        logging.debug(message)
def load_dataset(dataset):
    granularity = get_granularity(dataset)
    if granularity =='argument':
        path = get_path_preprocessed_arguments(dataset)
        df_arguments = pd.read_csv(path,quotechar='"',sep=",",quoting=csv.QUOTE_ALL,encoding='utf-8',dtype={'argument-id':str})

        return df_arguments[['argument-id','argument']]

    else:
        path = get_path_preprocessed_documents(dataset)
        df_documents = pd.read_csv(path,quotechar='"',sep=",",quoting=csv.QUOTE_ALL,encoding='utf-8',dtype={'document-id':str})
        return df_documents[['document-id','document']]

def load_document_topic(corpus):
    granularity=get_granularity(corpus)
    if granularity=='document':
        path_document_topic=get_path_document_topic(corpus)
        df_documnt_topic=pd.read_csv(path_document_topic,sep=",",encoding="utf-8",dtype={'document-id':str,'topic-id':int})
        return df_documnt_topic
    else:
        path_argument_topic=get_path_argument_topic(corpus)
        df_argument_topic=pd.read_csv(path_argument_topic,sep=",",encoding="utf-8",dtype={'argument-id':str,'topic-id':int})
        return df_argument_topic.rename(columns={'argument':'document','argument-id':'document-id'})

def load_hashmap():
    path_hashmap=get_path_hashmap('argument-inventory','document-id','id')
    df_hashmap=pd.read_csv(path_hashmap,sep=",",quotechar='"',encoding="utf-8",dtype={'id':int,'document-id':str})
    return df_hashmap

def save_hashmap(df_corpora):
    path_hashmap=get_path_hashmap('argument-inventory','document-id','id')
    df_hash_map=df_corpora[['id','document-id','corpus']]
    df_hash_map.to_csv(path_hashmap,sep=",",quotechar='"',encoding="utf-8",index=False)
    logging.warning("saved hashmap at %s"%path_hashmap)

def  check_document_topics_exists(label_corpus):
    path_document_topics = get_path_document_topic(label_corpus)
    path_argument_topics = get_path_argument_topic(label_corpus)
    document_topics_exists = (path_document_topics!=None and os.path.exists(path_document_topics)) or (path_argument_topics!=None and os.path.exists(path_argument_topics))
    return document_topics_exists
def check_corpora_topics_exists(label_corpus):
    path_topic = get_path_preprocessed_topics(label_corpus)
    return path_topic!=None

def shuffle_split_and_save_argument_inventory(df_corpora):
    df_all_corpora = df_corpora.sample(frac=1)
    part_count = get_part_count('argument-inventory')
    parts = np.array_split(df_all_corpora,part_count)

    for i,df_part in enumerate(parts):
        path=get_path_preprocessed_documents_version('argument-inventory',str(i))

        df_part['document']=df_part.apply((lambda row: drop_separator(row['document'],"\",\"")),axis=1)
        df_part.to_csv(path,quotechar='"',sep=",",quoting=csv.QUOTE_ALL,columns=['id','ground-truth','document'],encoding="utf-8",index=False)
        logging.warning("saved %s with %d"%(str(i),df_part.shape[0]))

    logging.warning("%d documents"%df_corpora.shape[0])
    logging.warning("%d unique documents"%df_corpora['document-id'].unique().shape[0])

def produce_argument_inventory(debug=False):
    corpora = load_corpora_list()

    all_corpora_dfs=[]
    id=0
    ids_hasmap={}

    for label_corpus in corpora:
        check_corpora_topics_exists(label_corpus)
        logging.warning("preprocessing %s"%label_corpus)
        df_corpus= load_dataset(label_corpus)

        df_corpus.rename(columns={'argument-id':'document-id','argument':'document'},inplace=True)
        df_corpus['id']=-1
        df_corpus['document-id']=df_corpus['document-id'].astype(str)

        for record_index,record in tqdm(df_corpus.iterrows()):
            document_corpus_id = record['document-id']
            identifier= (document_corpus_id,label_corpus)
            log_debug("document id %s is being preproessed"%str(document_corpus_id),debug)
            ids_hasmap[id] =identifier
            df_corpus.loc[record_index,'id']=id
            log_debug("document id %s is given a new id %s"%(str(document_corpus_id),str(id)),debug)
            id = id + 1
        is_ground_truth=check_corpora_topics_exists(label_corpus)
        df_corpus['ground-truth']=is_ground_truth
        df_corpus['corpus']=label_corpus
        if is_ground_truth: logging.warning("corpus %s has ground truth information"%label_corpus)
        all_corpora_dfs.append(df_corpus)

    df_corpora=pd.concat(all_corpora_dfs)
    save_hashmap(df_corpora)
    shuffle_split_and_save_argument_inventory(df_corpora)

def produce_argument_inventory_ground_truth_topics(dataset,corpora):
    argument_inventory_preprocessed_topics=[]
    path_preprocessed_topics=get_path_preprocessed_topics(dataset)
    for label_corpus in corpora:
        path_corpus_topics = get_path_preprocessed_topics(label_corpus)
        if check_corpora_topics_exists(label_corpus):
            df_topics=pd.read_csv(path_corpus_topics,sep=",",quotechar='"',encoding="utf-8")
            argument_inventory_preprocessed_topics.append(df_topics)
    df_argument_inventory_preprocessed_topics=pd.concat(argument_inventory_preprocessed_topics)
    df_argument_inventory_preprocessed_topics.to_csv(path_preprocessed_topics,sep=",",quotechar='"',encoding="utf-8",index=False)

def select_corproa_documents(corpora,df_argument_inventory_part):
    df_hashmap=load_hashmap()
    df_hashmap=df_hashmap[df_hashmap['corpus'].isin(corpora)]
    corproa_ids=df_hashmap['id'].values
    df_argument_inventory_part=df_argument_inventory_part[df_argument_inventory_part['id'].isin(corproa_ids)]
    return  df_argument_inventory_part

def produce_argument_inventory_ground_truth(dataset,corpora=[]):
    part_count_argument_inventory= get_part_count('argument-inventory')
    part_count_argument_inventory_ground_truth= get_part_count(dataset)
    ground_truth_parts=[]
    for part in range(part_count_argument_inventory):
        logging.warning("reading argument inventory part %d"%part)
        path=get_path_preprocessed_documents_version('argument-inventory',str(part))
        df_part=pd.read_csv(path,sep=",",quotechar='"',encoding="utf-8")
        df_part=df_part[df_part['ground-truth']]
        if len(corpora)>0:
            df_part=select_corproa_documents(corpora,df_part)
        logging.warning("found %d documents with ground-truth"%df_part.shape[0])
        ground_truth_parts.append(df_part)
    df_ground_truth=pd.concat(ground_truth_parts)
    logging.warning("ground truth size is %d"%df_ground_truth.shape[0])
    parts = np.array_split(df_ground_truth,part_count_argument_inventory_ground_truth)

    for i,df_part in enumerate(parts):
        path=get_path_preprocessed_documents_version(dataset,str(i))
        df_part.to_csv(path,quotechar='"',sep=",",quoting=csv.QUOTE_ALL,columns=['id','document'],encoding="utf-8",index=False)
        logging.warning("saved %s with %d"%(str(i),df_part.shape[0]))


def produce_argument_inventory_document_topics(dataset,ontology,corpora,is_debug=False):
    path_argument_inventory_document_topics=get_path_document_topic_ontology(dataset,ontology)
    if is_debug:
        path_argument_inventory_document_topics_debug=path_argument_inventory_document_topics.replace('.csv','.debug.csv')
        path_argument_inventory_document_topics_debug_new_ids=path_argument_inventory_document_topics.replace('.csv','.new-ids.csv')

    path_corpora_topics_ground_truth=get_path_ground_truth_corpora('topic-inventory',ontology)
    df_corpora_topics_ground_truth=pd.read_csv(path_corpora_topics_ground_truth,sep=",",encoding="utf-8",dtype={'ontology-topic-id':str,'topic-id':int})
    #df_corpora_topics_ground_truth=df_corpora_topics_ground_truth[~df_corpora_topics_ground_truth['ontology-topic-id'].isin(["-1","-2"])]
    df_corpora_topics_ground_truth=df_corpora_topics_ground_truth[['topic-id','corpus','ontology-topic-id']]
    df_hashmap=load_hashmap()

    all_document_topics=[]
    counter=0

    for label_corpus in corpora:
        if check_corpora_topics_exists(label_corpus):
            counter=counter+1
            df_document_topic=load_document_topic(label_corpus)
            df_document_topic.drop_duplicates(['document-id','topic-id'],inplace=True)
            df_document_topic['corpus']=label_corpus
            logging.warning("%d: loading %d document topic pairs for corpus %s"%(counter,df_document_topic.shape[0],label_corpus))
            all_document_topics.append(df_document_topic)
    df_corpora_document_topics=pd.concat(all_document_topics)
    df_argument_inventory_document_topics=df_corpora_document_topics.merge(df_hashmap,on=['document-id','corpus'])
    df_argument_inventory_document_topics_ontology_topic_ids=df_argument_inventory_document_topics.merge(df_corpora_topics_ground_truth,on=['topic-id','corpus'])
    df_argument_inventory_document_topics_ontology_topic_ids.to_csv(path_argument_inventory_document_topics,index=False,columns=['id','ontology-topic-id'],sep=",",encoding="utf-8",quotechar='"',quoting=csv.QUOTE_ALL)
    logging.warning("saving %d document topic pairs with ontology topic ids"%df_argument_inventory_document_topics_ontology_topic_ids.shape[0])
    if is_debug:
        df_corpora_document_topics.to_csv(path_argument_inventory_document_topics_debug,index=False,quotechar='"',quoting=csv.QUOTE_ALL,sep=",",encoding="utf-8")
        logging.warning("saving %d document topic pairs with prerprocessed topic ids"%df_corpora_document_topics.shape[0])
        df_argument_inventory_document_topics.to_csv(path_argument_inventory_document_topics_debug_new_ids,index=False  ,quotechar='"',quoting=csv.QUOTE_ALL,sep=",",encoding="utf-8")
        logging.warning("saving %d document topic pairs with new document ids"%df_argument_inventory_document_topics.shape[0])


def validate_argument_inventory_document_topics(dataset,ontology):
    path_argument_inventory_document_topics=get_path_document_topic_ontology(dataset,ontology)
    path_argument_inventory_document_topics_debug=path_argument_inventory_document_topics.replace('.csv','.debug.csv')
    df_hashmap=load_hashmap()

    path_argument_inventory_document_topics_debug_new_ids=path_argument_inventory_document_topics.replace('.csv','.new-ids.csv')
    df_corpora_document_topics=pd.read_csv(path_argument_inventory_document_topics_debug,sep=",",encoding="utf-8")
    df_argument_inventory_document_topics_new_ids=pd.read_csv(path_argument_inventory_document_topics_debug_new_ids,sep=",",encoding="utf-8")

    print("original\n")
    print(df_corpora_document_topics['corpus'].value_counts(sort=True))
    print("hashmap\n")
    print(df_hashmap['corpus'].value_counts(sort=True))
    print("new ids\n")
    print(df_argument_inventory_document_topics_new_ids['corpus'].value_counts(sort=True))

