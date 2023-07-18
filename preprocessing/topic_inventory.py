from conf.configuration import *
import pandas as pd
import wikipedia
import logging
import csv
import inflect
import re
topic_id=0

inflect_engine = inflect.engine()

def hash_or_return(topic,topic_id_map):
    global topic_id
    if topic not in topic_id_map:
        topic_id_map[topic]=topic_id
        topic_id=topic_id+1
    return topic_id_map[topic]

def clean_topic_articles(topic):
    topic=topic.lower()
    if topic.startswith('a '):
        topic= topic[2:]
    if topic.startswith('the '):
        topic= topic[4:]
    inflected_topic=inflect_engine.singular_noun(topic)
    if inflected_topic !=False:
        topic=inflected_topic
    return topic.strip()
def clean_topic_cliches(topic):
    cliches=load_cliches()
    for cliche in cliches:
        topic=re.sub(r"(\s|^)"+cliche+"(\s|$)"," ",topic)

    topic=re.sub(r"\s\s+","",topic)
    print(topic)
    return topic.strip()

def produce_corpora_topics():
    all_df_topics=[]
    topic_id_map={}
    for corpus in load_corpora_list():
        path_topics = get_path_preprocessed_topics(corpus)
        if path_topics!=None:
            df_topics=pd.read_csv(path_topics,sep=",",encoding="utf-8",dtype={"topic":str})
            df_topics['corpus']=corpus
            all_df_topics.append(df_topics)

    df_topic_source = pd.concat(all_df_topics)
    df_topic_source.rename(columns={'topic':'original-topic'},inplace=True)
    df_topic_source['topic']=[clean_topic_articles(topic) for topic in df_topic_source['original-topic']]
    df_topic_source['id']=[hash_or_return(topic,topic_id_map) for topic in df_topic_source['topic']]
    path_topic_inventory=get_path_source_part('topic-inventory', 'corpora-topics')

    df_topic_source.to_csv(path_topic_inventory,sep=",",encoding="utf-8",index=False)

    path_preprocessed_topics=get_path_preprocessed_part('topic-inventory','corpora-topics')
    df_topic=df_topic_source[['topic','id']]
    df_topic.drop_duplicates(['topic','id'],inplace=True)
    df_topic.to_csv(path_preprocessed_topics,sep=",",encoding="utf-8",index=False)

def produce_corpora_topics_description_candidates():
    path_preprocessed_topics=get_path_preprocessed_part('topic-inventory','corpora-topics')
    path_preprocessed_topics_desc_cand=get_path_preprocessed_part('topic-inventory','corpora-topics-description-candidates')
    print(path_preprocessed_topics_desc_cand)
    df_topics=pd.read_csv(path_preprocessed_topics,sep=",",encoding="utf-8",dtype={'topic':str})
    df_topics=df_topics[df_topics['error']==3]
    df_topics['topic']=df_topics['topic'].astype(str)

    topics=[]
    ids=[]
    description_candidates=[]

    df_topics_description_candidates={'topic':topics,'id':ids,'description-candidate':description_candidates}

    for i,row in df_topics.iterrows():
        disambiguations=[]
        topic_cleanded=clean_topic_cliches(row['topic'])
        pages=wikipedia.search(topic_cleanded)
        for page_title in pages:
            try:
                page=wikipedia.page(title=page_title)
                topics.append(row['topic'])
                ids.append(row['id'])
                description_candidates.append(page_title+": "+page.summary.replace("\"","\'"))
            except wikipedia.exceptions.DisambiguationError as e:
                disambiguations.extend(e.options)
            except Exception as error:
                logging.warning("no description for %s"%row['topic'])
        for disambiguation in disambiguations:
            try:
                page=wikipedia.page(title=disambiguation)
                topics.append(row['topic'])
                ids.append(row['id'])
                description_candidates.append(disambiguation+": "+page.summary.replace("\"","\'"))
            except Exception as error:
                logging.warning("no description for %s"%row['topic'])
    df_topics_description_candidates['suitable']=0
    pd.DataFrame(df_topics_description_candidates).to_csv(path_preprocessed_topics_desc_cand,sep=",",encoding="utf-8",index=False,quoting=csv.QUOTE_ALL)

def produce_ontologies_topics():
    all_topic_ontologies=[]
    for ontology in get_topic_ontologies():
        path_ontology_topics=get_path_topics('ontology-'+ontology)
        df_ontology_topics=pd.read_csv(path_ontology_topics,sep=",",encoding="utf-8")
        all_topic_ontologies.append(df_ontology_topics)
    df_all_topic_ontologies=pd.concat(all_topic_ontologies)
    df_all_topic_ontologies['topic']=df_all_topic_ontologies.apply(lambda x:x['name'].lower(),axis=1)
    del df_all_topic_ontologies['name']
    path_preprocessed_ontologies_topics=get_path_preprocessed_part('topic-inventory','ontologies-topics')
    df_all_topic_ontologies.to_csv(path_preprocessed_ontologies_topics,index=False)

def produce_ontologies():
    path_preprocessed_ontologies_topics=get_path_preprocessed_part('topic-inventory','ontologies')
    all_ontologies=[]
    for ontology in get_topic_ontologies():
        path_source_ontology=get_path_source('ontology-'+ontology)
        df_source_ontology=pd.read_csv(path_source_ontology,sep=",",encoding="utf-8")
        all_ontologies.append(df_source_ontology)
    df_all_ontologies=pd.concat(all_ontologies)
    df_all_ontologies.to_csv(path_preprocessed_ontologies_topics,sep=",",encoding="utf-8",index=False)

def prepare_corpora_topics_with_description():
    path_preprocessed_topics = get_path_preprocessed_part('topic-inventory','corpora-topics')
    path_preprocessed_topics_descriptions = get_path_preprocessed_part('topic-inventory','corpora-topics-description')
    df_preprocessed_topics_descriptions = pd.read_csv(path_preprocessed_topics_descriptions,sep=",",encoding="utf-8",quoting=csv.QUOTE_ALL)
    df_preprocessed_topics_descriptions = df_preprocessed_topics_descriptions[['id','description-candidate','suitable']]
    df_preprocessed_topics_descriptions = df_preprocessed_topics_descriptions[df_preprocessed_topics_descriptions['suitable']==1]
    df_preprocessed_topics = pd.read_csv(path_preprocessed_topics,sep=",",encoding="utf-8",dtype={'topic':str})
    #TODO skip following run and rerun
    df_preprocessed_topics=df_preprocessed_topics[df_preprocessed_topics['error'].isin([3])]
    #df_preprocessed_topics=df_preprocessed_topics[df_preprocessed_topics['agreement-study'].isin([0,1])]
    df_topics_with_description=df_preprocessed_topics.merge(df_preprocessed_topics_descriptions,on='id',how='left')


    df_topics_with_description['topic']=df_topics_with_description['topic'].astype(str)
    df_topics_with_description['description-candidate']=df_topics_with_description['description-candidate'].astype(str)
    df_topics_with_description['topic-with-description']=df_topics_with_description.apply(lambda row:(row['topic']+"\n==========\n"+row['description-candidate']) if isinstance(row['description-candidate'],str)  and len(row['description-candidate'])> 10 else row['topic'],axis=1)
    return df_topics_with_description

def prepare_corpora_topics_for_annotation():
    path_corpora_topics_for_annotation = get_path_preprocessed_part('topic-inventory','corpora-topics-annotation')
    df_preprocessed_topics=prepare_corpora_topics_with_description()
    df_preprocessed_topics['corpus']=""
    df_preprocessed_topics.sort_values('id',inplace=True)
    df_preprocessed_topics.rename(columns={'id':'document.id','topic-with-description':'text'},inplace=True)
    df_preprocessed_topics.to_csv(path_corpora_topics_for_annotation,columns=['document.id','text','corpus'],sep=",",encoding="utf-8",quotechar="\"",index=False)



def produce_new_corpora_topics():
    all_df_topics=[]

    for corpus in load_corpora_list('new-corpora-3'):
        path_topics = get_path_preprocessed_topics(corpus)
        if path_topics!=None and os.path.exists(path_topics):
            df_topics=pd.read_csv(path_topics,sep=",",encoding="utf-8",dtype={"topic":str})
            df_topics['corpus']=corpus
            all_df_topics.append(df_topics)

    df_topic_source = pd.concat(all_df_topics)
    df_topic_source.rename(columns={'topic':'original-topic'},inplace=True)
    path_new_corpora=get_path_source_part('topic-inventory','corpora-topics-new-3')

    df_topic_source.to_csv(path_new_corpora,sep=",",encoding="utf-8",index=False)


def clean_new_corpora_topics():
    """
    automatically clean topic labels by dropping stance words and clichees. The cleaned topic labels are stored in the column
    automatic-cleaned
    :return:
    """
    path_new_topics_new=get_path_source_part('topic-inventory','corpora-topics-new-3')
    df_corpora_topics_new = pd.read_csv(path_new_topics_new,sep=",",encoding="utf-8")
    if 'automatic-cleaned' in df_corpora_topics_new.columns:
        del df_corpora_topics_new['automatic-cleaned']

    df_corpora_topics_new['automatic-cleaned']=df_corpora_topics_new['original-topic'].apply(lambda t: t.lower().replace("?","").strip())
    df_corpora_topics_new['automatic-cleaned']=df_corpora_topics_new['automatic-cleaned'].apply(lambda topic: clean_topic_cliches(topic))
    df_corpora_topics_new['automatic-cleaned']=df_corpora_topics_new['automatic-cleaned'].apply(lambda topic: clean_topic_articles(topic))
    df_corpora_topics_new.to_csv(path_new_topics_new,sep=",",encoding="utf-8",index=False)

def add_new_preprocessed_topic_ids():

    path_new_topics = get_path_source_part('topic-inventory','corpora-topics-new-3')
    df_corpora_topics_new=pd.read_csv(path_new_topics,sep=",",quotechar='\"',encoding="utf-8")
    df_corpora_topics_new.info()
    df_corpora_topics_new_matched=df_corpora_topics_new[~df_corpora_topics_new['id'].isna()]
    df_corpora_topics_new.sort_values('topic-complex',inplace=True)
    df_corpora_topics_new['matched']=True
    topic_ids={}
    counter = df_corpora_topics_new_matched['id'].max() + 1
    for topic_index,topic_record in df_corpora_topics_new.iterrows():
        if pd.isnull(df_corpora_topics_new.loc[topic_index,'id']):

            topic_id=topic_ids.get(topic_record['topic'],counter)
            if topic_id==counter:
                topic_ids[topic_record['topic']]=topic_id
                counter = counter + 10
            df_corpora_topics_new.loc[topic_index,'matched']=False
            df_corpora_topics_new.loc[topic_index,'id'] = topic_id
    df_corpora_topics_new.to_csv(path_new_topics,sep=",",quotechar='\"',encoding="utf-8",index=False)

def update_new_preprocessed_topic_ids():
    """
    automatically add new ids to the preprocessed topics
    :return:
    """
    path_new_topics = get_path_source_part('topic-inventory','corpora-topics-new-3')
    df_corpora_topics_new=pd.read_csv(path_new_topics,sep=",",quotechar='\"',encoding="utf-8")
    df_corpora_topics_new_matched=df_corpora_topics_new[df_corpora_topics_new['matched']]
    df_corpora_topics_new.sort_values('topic-complex',inplace=True)
    topic_ids={}
    counter = df_corpora_topics_new_matched['id'].max() + 1
    for topic_index, topic_record in df_corpora_topics_new.iterrows():
        if not df_corpora_topics_new.loc[topic_index,'matched']:
            topic_id = topic_ids.get(topic_record['topic'],counter)
            if topic_id == counter:
                topic_ids[topic_record['topic']] = topic_id
                counter = counter + 10
            df_corpora_topics_new.loc[topic_index,'id'] = topic_id
    df_corpora_topics_new.to_csv(path_new_topics,sep=",",quotechar='\"',encoding="utf-8",index=False)

def add_new_preprocessed_topics():
    """
    add the new preprocessed topics to the main preprprocessed topics file
    :return:
    """
    path_new_corpora_topics = get_path_source_part('topic-inventory','corpora-topics-new-3')
    path_preprocessed_topics = get_path_preprocessed_part('topic-inventory','corpora-topics')
    df_new_corpora_topics = pd.read_csv(path_new_corpora_topics,sep=",",quotechar='\"', encoding="utf")
    df_new_corpora_topics=df_new_corpora_topics[~df_new_corpora_topics['matched']]
    df_new_corpora_topics=df_new_corpora_topics[['topic','id']].drop_duplicates(['topic','id'])
    df_new_corpora_topics['id']=df_new_corpora_topics['id'].astype(int)
    df_new_corpora_topics['error']=3
    df_preprocessed_topics=pd.read_csv(path_preprocessed_topics,sep=",",quotechar="\"",encoding="utf-8")
    df_preprocessed_topics = pd.concat([df_preprocessed_topics,df_new_corpora_topics])
    df_preprocessed_topics.to_csv(path_preprocessed_topics,sep=",",quotechar="\"",encoding="utf-8",index=False)

def add_new_corpora_topics():
    path_new_corpora_topics = get_path_source_part('topic-inventory','corpora-topics-new-3')
    path_corpora_topics = get_path_source_part('topic-inventory','corpora-topics')
    df_new_corpora_topics = pd.read_csv(path_new_corpora_topics,sep=",",quotechar='\"', encoding="utf")
    df_new_corpora_topics = df_new_corpora_topics[['topic-id','original-topic','corpus','topic','id']]
    df_new_corpora_topics['id']=df_new_corpora_topics['id'].astype(int)
    df_corproa_topics = pd.read_csv(path_corpora_topics,sep=",",quotechar='\"',encoding="utf-8")
    df_corproa_topics_merged = pd.concat([df_corproa_topics, df_new_corpora_topics])
    df_corproa_topics_merged.to_csv(path_corpora_topics,sep=",",quotechar="\"",encoding="utf-8",index=False,columns=['id','topic-id','corpus','original-topic','topic'])

def update_topic_descriptions_ids():
    path_new_corpora_topics = get_path_source_part('topic-inventory','corpora-topics-new-2')
    df_new_corpora_topics = pd.read_csv(path_new_corpora_topics,sep=",",quotechar='\"', encoding="utf",index_col='old-id',dtype={'id':int,'old-id':int})
    df_new_corpora_topics=df_new_corpora_topics[~df_new_corpora_topics['matched']]
    df_new_corpora_topics=df_new_corpora_topics[['id']]
    id_map=df_new_corpora_topics.to_dict()['id']
    path_preprocessed_topics_desc_cand=get_path_preprocessed_part('topic-inventory','corpora-topics-description-candidates')
    df_topics_candidates=pd.read_csv(path_preprocessed_topics_desc_cand,sep=",",encoding="utf-8",dtype={'id':int,'topic':str})
    df_topics_candidates.info()
    df_topics_candidates['id'] = df_topics_candidates['id'].apply(lambda old_id: id_map[old_id] if old_id in id_map else(-1))
    df_topics_candidates.to_csv(path_preprocessed_topics_desc_cand,sep=",",quotechar="\"",encoding="utf-8",index=False)

    path_preprocessed_topics_desc=get_path_preprocessed_part('topic-inventory','corpora-topics-description')
    df_topics_described=pd.read_csv(path_preprocessed_topics_desc,sep=",",encoding="utf-8",dtype={'id':int,'topic':str})
    df_topics_described['id']=df_topics_described['id'].apply(lambda old_id: id_map[old_id] if old_id in id_map else(-1))
    df_topics_described.to_csv(path_preprocessed_topics_desc,sep=",",quotechar="\"",encoding="utf-8",index=False)

