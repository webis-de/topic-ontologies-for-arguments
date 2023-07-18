import json

import pandas as pd
import os
from conf.configuration import *
def sample_agreement_study_topics(n):
    path_preprocessed_topics=get_path_preprocessed_part('topic-inventory','corpora-topics')
    df=pd.read_csv(path_preprocessed_topics,sep=",",encoding="utf-8")
    df_smaple=df.sample(n)
    df['agreement-study']=0
    for i,record in df_smaple.iterrows():
        df.loc[i,'agreement-study']=1

    df.to_csv(path_preprocessed_topics,sep=",",encoding="utf-8",index=False)



def filter_topic_matches():

    annotator_per_ontology ={"wikipedia":"yamen",
                             'wikipedia-categories':'yamen',
                             'strategic-intelligence':'johannes',
                             'strategic-intelligence-sub-topics': 'johannes',
                             'debatepedia':'martin'
    }
    path_preprocessed_topics=get_path_preprocessed_part('topic-inventory','corpora-topics')
    df_topics = pd.read_csv(path_preprocessed_topics,sep=",",encoding="utf-8")
    df_topics = df_topics[df_topics['agreement-study']==1]
    documents = []
    topic_ids = []
    for ontology in get_topic_ontologies():

        path = f"/mnt/ceph/storage/data-in-progress/data-research/arguana/topic-ontologies/topic-matching/{ontology}/judgements.json"
        with open(path,'r') as stream:
            data = json.load(stream)
            annotator = annotator_per_ontology[ontology]
            for topic in data[annotator]:
                if int(topic) in df_topics['id'].values:
                    matched_ontology_topics = data[annotator][topic].keys()
                    document_id = topic+"_"+ontology
                    documents += [document_id for value in matched_ontology_topics]
                    topic_ids += matched_ontology_topics
    df = pd.DataFrame({'document.id':documents, 'topic.id':topic_ids})
    df['method'] = 'exact-match'
    df['score'] = 0
    df.sort_values('document.id', inplace=True)
    path = get_path_judgements_model('topic-matching-pilot','all-bm25')
    df.info()
    df.to_csv(path, sep=",", encoding="utf-8",index=False)


def filter_documents():
    path_corpora_topics_for_annotation = get_path_preprocessed_part('topic-inventory','corpora-topics-annotation')
    path_documents = get_documents_path('topic-matching-pilot','all-bm25')
    path_judgments = get_path_judgements_model('topic-matching-pilot','all-bm25')
    df_judgments = pd.read_csv(path_judgments,sep=",")
    df_judgments['document.id.int'] = df_judgments['document.id'].apply(lambda id:int(id.split("_")[0]))
    df_judgments = df_judgments[['document.id.int','document.id']]
    df_judgments.drop_duplicates("document.id",inplace=True)
    df_judgments.rename(columns={"document.id":"document_id"},inplace=True)
    df_corpora_topics_for_annotations = pd.read_csv(path_corpora_topics_for_annotation,sep=",",encoding="utf-8")
    df_judgments.info()
    df_documents_for_annotation = df_judgments.merge(df_corpora_topics_for_annotations, left_on='document.id.int', right_on='document.id')
    del df_documents_for_annotation['document.id']

    df_documents_for_annotation.rename(columns={"document_id":"document.id"},inplace=True)

    df_documents_for_annotation.to_csv(path_documents,columns=['document.id','text','corpus'],sep=",",quotechar="\"",encoding="utf-8",index=False)

if __name__=="__main__":
    #sample_agreement_study_topics(104)
    filter_topic_matches()
    filter_documents()