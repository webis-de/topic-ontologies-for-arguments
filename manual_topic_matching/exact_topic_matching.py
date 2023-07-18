import pandas as pd
from conf.configuration import *
from manual_topic_matching.bm25_topic_matching import *
import spacy as sp
import re
sp = sp.load("en_core_web_lg")


def drop_stop_words(tokens):
    all_stopwords = sp.Defaults.stop_words
    tokens_without_sw= [word for word in tokens if not word in all_stopwords]
    return tokens_without_sw

def tokenize(text):

    tokens=text.split(" ")
    tokens = [token.lower() for token in tokens]
    return drop_stop_words(tokens)

def exact_match(corpus_topic,ontology_topic):
    corpus_topic_tokenized =tokenize(corpus_topic)
    ontology_topic_tokenized = tokenize(ontology_topic)
    corpus_topic=" ".join(corpus_topic_tokenized)
    ontology_topic=" ".join(ontology_topic_tokenized)
    return corpus_topic == ontology_topic


def produce_judgements(similarity_function,ontology):
    paht_judgements_exact_matches=get_path_judgements_model('topic-matching',ontology+"-exact")
    path_left_topics=get_path_judgements_model('topic-matching',ontology+"-left")
    path_corpora_topics= get_path_preprocessed_part('topic-inventory','corpora-topics')
    df_corpora_topics=pd.read_csv(path_corpora_topics,sep=",",encoding="utf-8")
    df_ontology_topics=load_ontology_dataset(ontology)


    corpora_topics=[]
    ontology_topics=[]
    corpora_topic_ids=[]
    ontology_topic_ids=[]
    left_topics=[]
    left_topic_ids=[]
    for i,corpus_topic_record in df_corpora_topics.iterrows():
        topic=corpus_topic_record['topic']
        corpus_topic_id=corpus_topic_record['id']
        match_found=False
        for i, ontology_topic_record in df_ontology_topics.iterrows():
            if similarity_function(topic,ontology_topic_record['name']):
                corpora_topics.append(topic)
                corpora_topic_ids.append(corpus_topic_id)
                ontology_topics.append(ontology_topic_record['name'])
                ontology_topic_ids.append(ontology_topic_record['topic.id'])
                match_found=True
        if not match_found:
            left_topics.append(topic)
            left_topic_ids.append(corpus_topic_id)


    df_judgements=pd.DataFrame({'corpus-topic':corpora_topics,'corpus-topic-id':corpora_topic_ids,'ontologies-topic':ontology_topics,'ontologies-topic-id':ontology_topic_ids})
    df_judgements.to_csv(paht_judgements_exact_matches,sep=",",encoding="utf-8",index=False)
    df_left_topics=pd.DataFrame({'topic':left_topics,'id':left_topic_ids})
    df_left_topics.to_csv(path_left_topics,sep=",",encoding="utf-8",index=False)


