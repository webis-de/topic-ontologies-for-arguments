import pandas as pd
from conf.configuration import *
import csv
def generate_topics():
    path_topics_debatepedia= get_path_topics('ontology-debatepedia')
    path_topics_wikipedia= get_path_topics('ontology-wikipedia')
    path_topics_strategic_intelligence= get_path_topics('ontology-strategic-intelligence')
    path_topics_strategic_intelligence_sub_topics= get_path_topics('ontology-strategic-intelligence-sub-topics')
    path_topics_experiment = get_path_topics('topic-modeling-experiment')
    df_topics_debatepedia=pd.read_csv(path_topics_debatepedia,sep=',',quotechar='"',quoting=csv.QUOTE_ALL,encoding='utf-8',index_col='id')
    df_topics_wikipedia=pd.read_csv(path_topics_wikipedia,sep=',',quotechar='"',quoting=csv.QUOTE_ALL,encoding='utf-8',index_col='id')
    df_topics_strategic_intelligence=pd.read_csv(path_topics_strategic_intelligence,sep=',',quotechar='"',quoting=csv.QUOTE_ALL,encoding='utf-8',index_col='id')
    df_topics_strategic_intelligence_sub_topics=pd.read_csv(path_topics_strategic_intelligence_sub_topics,sep=',',quotechar='"',quoting=csv.QUOTE_ALL,encoding='utf-8',index_col='id')
    df_topics_debatepedia.info()
    df_topics_wikipedia.info()
    df_topics_strategic_intelligence.info()
    df_topics_experiment= pd.concat([df_topics_debatepedia,df_topics_strategic_intelligence,df_topics_wikipedia,df_topics_strategic_intelligence_sub_topics])
    df_topics_experiment.info()
    df_topics_experiment.sort_index().to_csv(path_topics_experiment,sep=',',encoding='utf-8')

generate_topics()

def generate_topic_suggestions():
    ontologies= ['debatepedia','wikipedia','strategic-intelligence','strategic-intelligence-sub-topics','wikipedia-categories']
    models = ['word2vec-esa-100']
    path_sample_all_ontologies =get_path_top_k_topics_per_document('topic-modeling-experiment','cmv-all-ontologies','word2vec-esa-100',10)
    all_models_data_frames=[]
    for model in models:
        top_topic_data_frames=[]
        for ontology in ontologies:
            path_top_topics= get_path_top_k_topics_per_document('sample-cmv',ontology,model,10)
            df_top_topics = pd.read_csv(path_top_topics,sep=',',quotechar='"',quoting=csv.QUOTE_ALL,encoding='utf-8',index_col='document.id',dtype={'topic.id': object})
            top_topic_data_frames.append(df_top_topics)
        df_model_topics = pd.concat(top_topic_data_frames)
        df_model_topics ['method']=[model for index in df_model_topics.index]
        all_models_data_frames.append(df_model_topics)
    df_all = pd.concat(all_models_data_frames)
    df_all.to_csv(path_sample_all_ontologies,sep=',',quotechar='"',quoting=csv.QUOTE_ALL,encoding='utf-8')

generate_topic_suggestions()