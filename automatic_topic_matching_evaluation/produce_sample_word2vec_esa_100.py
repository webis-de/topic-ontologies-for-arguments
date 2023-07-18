import pandas as pd
from conf.configuration import *
import csv
from topic_modeling.topics import *

def generate_all_topic_suggestions():
    ontologies= ['debatepedia','wikipedia','strategic-intelligence','strategic-intelligence-sub-topics','wikipedia-categories']
    models = ['word2vec-esa-100']
    path_sample_all_ontologies =get_path_all_topics_per_document('topic-modeling-experiment','all-ontologies','word2vec-esa-100')
    print(path_sample_all_ontologies)
    all_models_data_frames=[]

    for model in models:
        all_topic_data_frames=[]
        for ontology in ontologies:
            topics,topic_ids=load_topics_with_ids("ontology-"+ontology)
            k = len(topics)
            path_all_topics_sample_cmv= get_path_top_k_topics_per_document('sample-cmv',ontology,model,k)
            path_all_topics_sample= get_path_top_k_topics_per_document('sample',ontology,model,k)
            df_all_topics_sample = pd.read_csv(path_all_topics_sample,sep=',',quotechar='"',quoting=csv.QUOTE_ALL,encoding='utf-8',index_col='document.id',dtype={'topic.id': object})
            df_all_topics_sample_cmv = pd.read_csv(path_all_topics_sample_cmv,sep=',',quotechar='"',quoting=csv.QUOTE_ALL,encoding='utf-8',index_col='document.id',dtype={'topic.id': object})
            print(ontology)
            print(df_all_topics_sample.info())
            print(df_all_topics_sample_cmv.info())
            all_topic_data_frames.append(df_all_topics_sample)
            all_topic_data_frames.append(df_all_topics_sample_cmv)
        df_model_topics = pd.concat(all_topic_data_frames)
        df_model_topics ['method']=[model for index in df_model_topics.index]
        all_models_data_frames.append(df_model_topics)
    df_all = pd.concat(all_models_data_frames)
    df_all=df_all.sort_values('topic.id')
    df_all.to_csv(path_sample_all_ontologies,sep=',',quotechar='"',quoting=csv.QUOTE_ALL,encoding='utf-8')
generate_all_topic_suggestions()