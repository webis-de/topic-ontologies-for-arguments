from whoosh import index
from whoosh import fields
from whoosh import qparser
from whoosh.qparser import OrGroup
from pathlib import Path
from conf.configuration import *
import pandas as pd
import os
from whoosh.analysis import StandardAnalyzer
import logging
from datetime import datetime
def setup_search_log():
    logging.basicConfig(format="%(message)s",filename="../logs/search.log",level=logging.DEBUG)
    logging.warning(datetime.now())

def check_and_create(path):
    if not os.path.exists(path):
        os.makedirs(path)

def create_schema():
    st_ana = StandardAnalyzer()
    schema = fields.Schema(id=fields.STORED,
                           name=fields.STORED,
                           text=fields.TEXT(analyzer=st_ana, stored=True),
                           )
    return  schema

def load_ontology_dataset(ontology):
    path_source_topic=get_path_source_part('ontology-' + ontology, 'topics')
    path_source_texts=get_path_source_part('ontology-' + ontology, 'texts')
    df_ontology_topics=pd.read_csv(path_source_topic,sep=",",encoding="utf-8",dtype={'topic.id':str})
    df_ontology_texts=pd.read_csv(path_source_texts,sep=",",encoding="utf-8",dtype={'topic.id':str})
    df_ontology_texts=df_ontology_texts[['topic.id','text']]
    df_ontology_topics=df_ontology_topics[['topic.id','name']]
    return df_ontology_texts.merge(df_ontology_topics,on='topic.id')

def build_index(ontology):
    logging.warning("indexing ontology %s"%ontology)

class DummySearchEngine:

    def __init__(self,ontology,limit):
        df_ontology=load_ontology_dataset(ontology)

        self.documents=[]
        for _,row in df_ontology.iterrows():
            self.documents.append((str(row['topic.id']),row['name'],1))

    def index(self):
        None

    def search(self,query):
        return self.documents

class SearchEngine:
    def __init__(self,ontology,limit):
        self.path_index=path_bm25_index=get_path_source_part('ontology-' + ontology, 'index')
        index_path=Path(path_bm25_index)

        self.limit=limit
        self.ontology= ontology
        if os.listdir(index_path):
            self.ix = index.open_dir(index_path)
        else:
            self.index()

    def index(self):
        logging.warning("indexing %s"%self.ontology)
        df_ontology=load_ontology_dataset(self.ontology)
        path_bm25_index=get_path_source_part('ontology-' + self.ontology, 'index')
        index_path= Path(path_bm25_index)
        check_and_create(index_path)
        schema = create_schema()
        self.ix = index.create_in(index_path, schema)
        writer = self.ix.writer()
        for i,topic_record in df_ontology.iterrows():
            logging.warning("indexing %s"%str(topic_record['topic.id']))
            writer.add_document(id=str(topic_record['topic.id']),name=topic_record['name'],text=topic_record['text'])
        writer.commit()

    def search(self,query):
        similar_topics=[]
        with self.ix.searcher() as searcher:
            qp = qparser.QueryParser("text", schema=self.ix.schema, group=OrGroup)
            q= qp.parse(query)
            results = searcher.search(q, limit=self.limit)
            rank =0
            for res in results:
                rank=rank+1
                name= res['name']
                id= res['id']

                similar_topics.append((id,name,rank))
        return similar_topics




def build_indices():

    for ontology in get_topic_ontologies():
        build_index(ontology)


def match_topics():
    setup_search_log()
    search_engines= {}
    for ontology in get_topic_ontologies():
        logging.warning('looking up %s\'s topics'%ontology)
        #path_left_topics=get_path_judgements_model('topic-matching',ontology+"-left")
        path_corpora_topics= get_path_preprocessed_part('topic-inventory','corpora-topics')
        path_no_matches=get_path_judgements_model('topic-matching',ontology+"-no-matches")
        df_corpora_topics =pd.read_csv(path_corpora_topics,sep=",",encoding="utf-8")
        #TODO skip following run and rerun
        df_corpora_topics=df_corpora_topics[df_corpora_topics['error'].isin([3])]
        #df_corpora_topics=df_corpora_topics[df_corpora_topics['agreement-study'].isin([1])]
        topics=[]
        ids=[]
        ontology_topics=[]
        ontology_topic_ids=[]
        ontology_topic_rankings=[]
        topics_no_matches=[]
        ids_no_matches=[]
        path_judgements= get_path_judgements_model('topic-matching',ontology+"-bm25")
        if ontology!='wikipedia-categories':
            search_engines[ontology]=SearchEngine(ontology,50)
        else:
            search_engines[ontology]=DummySearchEngine(ontology,50)

        for index, topic_record in df_corpora_topics.iterrows():
            id =topic_record['id']
            topic=topic_record['topic']
            logging.warning("looking up %s"%id)
            matching_results=search_engines[ontology].search(topic_record['topic'])
            logging.warning("found %d matches"%len(matching_results))
            if len(matching_results)==0:
                topics_no_matches.append(topic)
                ids_no_matches.append(id)
                logging.warning("not matches found for %s"%id)
            for ontology_topic_id, ontology_topic, ontology_topic_rank in matching_results:
                topics.append(topic)
                ids.append(id)
                ontology_topics.append(ontology_topic)
                ontology_topic_ids.append(ontology_topic_id)
                ontology_topic_rankings.append(ontology_topic_rank)
        df_topic_no_matches=pd.DataFrame({'topic':topics_no_matches,'id':ids_no_matches})
        df_topic_no_matches.to_csv(path_no_matches,sep=",",encoding="utf-8",index=False)

        df_topic_matches=pd.DataFrame({'topic':topics,'id':ids,'ontology-topic':ontology_topics,'ontology-topic-id':ontology_topic_ids,'ontology-topic-rank':ontology_topic_rankings})
        df_topic_matches.to_csv(path_judgements,sep=",",encoding="utf-8",index=False)


def prepare_judgements_for_annotations(ontology):
    label_judgements_path='%s-for-annotation'%(ontology+"-"+"bm25")
    path_judgements_for_annotations=get_path_judgements_model('topic-matching',label_judgements_path)
    path_judgements= get_path_judgements_model('topic-matching',ontology+"-bm25")
    print(path_judgements_for_annotations)
    print(path_judgements)
    df_ontology_judgements=pd.read_csv(path_judgements,sep=",",encoding="utf",dtype={'ontology-topic-id':object})
    df_ontology_judgements=df_ontology_judgements[['id','ontology-topic-id']]
    df_ontology_judgements.sort_values('id',inplace=True)
    df_ontology_judgements.rename(columns={'id':'document.id','ontology-topic-id':'topic.id'},inplace=True)
    df_ontology_judgements['method']="exact-match"
    df_ontology_judgements['score']=0.0
    df_ontology_judgements.to_csv(path_judgements_for_annotations,columns=['document.id','topic.id','method','score'],sep=",",encoding="utf-8",index=False)
