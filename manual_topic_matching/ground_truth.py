from conf.configuration import *
import json
import pandas as pd
import logging
def parse_raw_annotations(path_raw,path_ground_truth):
    corpus_topic_ids=[]
    ontology_topic_ids=[]
    with open (path_raw) as json_file:
        data= json.load(json_file)
        if 'yamen' in data:
            documents=data['yamen']
        elif 'johannes' in data:
            documents=data['johannes']
        elif 'martin' in data:
            documents=data['martin']
        for document in documents:
            if document=='2617':
                continue
            document_annotations = documents[document]
            topic_in_ontology_found=False
            for ontology_topic in document_annotations:
                if document_annotations[ontology_topic]== True:
                    corpus_topic_ids.append(document)
                    ontology_topic_ids.append(str(ontology_topic)
                                              )
                    topic_in_ontology_found=True
            if not topic_in_ontology_found:
                corpus_topic_ids.append(document)
                ontology_topic_ids.append(str(-1))

        df_ground_truth=pd.DataFrame({'id':corpus_topic_ids,'ontology-topic-id':ontology_topic_ids})
        df_ground_truth['ontology-topic-id']=df_ground_truth['ontology-topic-id'].astype(str)
        df_ground_truth.to_csv(path_ground_truth,sep=",",encoding="utf-8",index=False)


def update_annotations(path_ground_truth,path_ground_truth_batch):
    df_ground_truth=pd.read_csv(path_ground_truth,sep=",",encoding="utf-8",dtype={'ontology-topic-id':str})
    df_ground_truth_batch=pd.read_csv(path_ground_truth_batch,sep=",",encoding="utf-8",dtype={'ontology-topic-id':str})

    df_ground_truth_batch_to_add= df_ground_truth_batch[~df_ground_truth_batch['id'].isin(df_ground_truth['id'])]
    df_ground_truth_batch_to_update= df_ground_truth_batch[df_ground_truth_batch['id'].isin(df_ground_truth['id'])]
    # drop those to update from
    df_ground_truth=df_ground_truth[~df_ground_truth['id'].isin(df_ground_truth_batch_to_update['id'])]
    df_ground_truth=pd.concat([df_ground_truth,df_ground_truth_batch_to_add,df_ground_truth_batch_to_update])
    df_ground_truth.to_csv(path_ground_truth,sep=",",encoding="utf-8",index=False)

def update_wikipedia_errors_and_missing():
    path_ground_truth_wikipedia=get_path_ground_truth('topic-inventory','wikipedia')
    path_ground_truth_wikipedia_errors_and_missing=get_path_ground_truth('topic-inventory','wikipedia-errors-and-missing')
    update_annotations(path_ground_truth_wikipedia,path_ground_truth_wikipedia_errors_and_missing)



def add_no_matches(path_ground_truth,path_no_matches):
    df_ground_truth=pd.read_csv(path_ground_truth,sep=",",encoding="utf-8",dtype={'ontology-topic-id':str})
    df_no_matched= pd.read_csv(path_no_matches,sep=",",encoding="utf-8")
    df_no_matched=df_no_matched[['id']]
    df_no_matched['ontology-topic-id']=-2
    df_ground_truth=pd.concat([df_ground_truth, df_no_matched])
    df_ground_truth.to_csv(path_ground_truth,sep=",",encoding="utf-8",index=False)

def produce_ground_truth_corpora(ontology):
    logging.warning("processing ground truth corpora for %s"%ontology)
    path_topic_inventory=get_path_source_part('topic-inventory', 'corpora-topics')
    path_ground_truth=get_path_ground_truth('topic-inventory',ontology)
    if os.path.exists(path_ground_truth):
        logging.warning("%s exists" %path_ground_truth)
        path_ground_truth_corpora=get_path_ground_truth_corpora('topic-inventory',ontology)
        df_topic_inventory=pd.read_csv(path_topic_inventory,sep=",",encoding="utf-8")
        df_ground_truth=pd.read_csv(path_ground_truth,sep=",",encoding="utf-8",dtype={'ontology-topic-id':str})
        df_ground_truth_corpora=df_topic_inventory.merge(df_ground_truth,on='id')
        df_ground_truth_corpora.to_csv(path_ground_truth_corpora,sep=",",encoding="utf-8",index=False,columns=['id','topic-id','corpus', \
                                                                                                   'ontology-topic-id'])
def produce_topic_groundtruth_all_ontologies():
    logging.basicConfig(filename="../logs/ground-truth-generation.log")

    ontologies= get_topic_ontologies()
    #ontologies.append('wikipedia-errors-and-missing')
    for ontology in ontologies:
        path_ground_truth=get_path_ground_truth('topic-inventory',ontology)
        path_raw_ground_truth=get_path_ground_truth_raw('topic-matching',ontology)
        if path_raw_ground_truth!=None and os.path.exists(path_raw_ground_truth):

            parse_raw_annotations(path_raw_ground_truth,path_ground_truth)
            logging.warning("parsed %s"%path_raw_ground_truth)
            path_documents_no_matches=get_path_judgements_model('topic-matching',ontology+'-no-matches')
            if ontology != 'wikipedia-errors-and-missing':
                add_no_matches(path_ground_truth,path_documents_no_matches)
        else:
            logging.warning("could not find %s"%path_raw_ground_truth)

    #update_wikipedia_errors_and_missing()



