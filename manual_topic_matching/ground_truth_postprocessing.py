import pandas as pd
import logging
import json
from preprocessing.topic_inventory_postprocessing import *
from automatic_topic_matching_evaluation.sample_to_html import path
from datetime import datetime
import copy
def setup_logging_duplicate():
    logging.basicConfig(filename="../logs/ground-truth-duplicates.log",format="%(message)s")

def setup_logging_new_ids():
    logging.basicConfig(filename="../logs/ground-truth-new-ids.log",format="%(message)s")

def setup_logging_merging_wikipedia_judgements():
    logging.basicConfig(filename="../logs/merging-wikipedia-judgements.log",format="%(message)s")

def  get_annotator_map():
    return {'wikipedia':"yamen",
            'wikipedia-categories':"yamen",
            'strategic-intelligence':'johannes',
            'strategic-intelligence-sub-topics':'johannes',
            'debatepedia':'martin'}
def get_documents(data,annotator):

    documents=data[annotator]
    return documents

def set_documents(data,documents,annotator):
    data[annotator]=documents

def drop_duplicates_from_judgements_raw(ontology):
    annotator_map=get_annotator_map()
    annotator=annotator_map[ontology]
    logging.warning(datetime.now())
    logging.warning("dropping duplicates for %s"%ontology)
    duplicate_topics = load_duplicate_topics_2()
    path_raw_ground_truth=get_path_ground_truth_raw('topic-matching',ontology)

    if path_raw_ground_truth!=None and os.path.exists(path_raw_ground_truth):
        with open (path_raw_ground_truth) as json_file:
            data= json.load(json_file)
            documents=get_documents(data,annotator)
            logging.warning("count of documents before dropping duplicates is %d"%(len(documents)))
            for document in list(documents):
                if int(document) in duplicate_topics.keys():
                    logging.warning("document id %d is matched"%int(document))
                    documents.pop(document)
            logging.warning("count of documents after dropping duplicates is %d"%(len(documents)))

        #path_raw_ground_truth=path_raw_ground_truth.replace("json","debug.json")
        logging.warning("saving to %s"%path_raw_ground_truth)
        with open(path_raw_ground_truth,'w') as json_file:
            json.dump(data,json_file)
    else:
        logging.warning("%s not found"%path_raw_ground_truth)

def drop_duplicates_all_ontologies():

    setup_logging_duplicate()
    ontologies= get_topic_ontologies()
    ontologies.append('wikipedia-errors-and-missing')
    for ontology in ontologies:
        drop_duplicates_from_judgements_raw(ontology)


def update_topic_ids_judgements_raw(ontology,drop_non_matched=False):
    annotator_map=get_annotator_map()
    annotator=annotator_map[ontology]
    logging.warning(datetime.now())
    logging.warning("updating topic ids for %s"%ontology)
    topic_id_map=load_new_topic_id_map()
    path_raw_ground_truth=get_path_ground_truth_raw_new('topic-matching',ontology)
    #path_raw_ground_truth_debug=path_raw_ground_truth.replace(".json",".debug.json")
    new_documents={}
    counter=0
    if path_raw_ground_truth!=None and os.path.exists(path_raw_ground_truth):
        with open (path_raw_ground_truth) as json_file:
            data= json.load(json_file)
            documents=get_documents(data,annotator)
            documents_copy=copy.deepcopy(documents)
            logging.warning("count of documents before updating ids is %d"%(len(documents)))
            for document_old in list(documents_copy):
                counter= counter +1
                if int(document_old) in topic_id_map.keys():

                    document=topic_id_map[int(document_old)]

                    annotations=documents_copy.pop(document_old)
                    new_documents[str(document)]=annotations
                    logging.warning("document id %s is updated with %s"%(document_old,document))
                else:
                    if drop_non_matched:
                        logging.warning("document id %s is missed"%document_old)
                    else:
                        annotations=documents_copy.pop(document_old)
                        new_documents[document_old]=annotations
                        logging.warning("document id %s is left as is"%document_old)
            logging.warning(f"count of documents is {counter}")
            logging.warning("documents after updating ids is %d"%(len(new_documents)))
            doc_keys = set(documents.keys())
            new_doc_keys = set(new_documents.keys())
            logging.warning(f"left documents are {sorted(doc_keys.difference(new_doc_keys))}")
            logging.warning(f"left documents are {sorted(new_doc_keys.difference(doc_keys))}")
        logging.warning("saving to %s"%path_raw_ground_truth)
        set_documents(data,new_documents,annotator)


        with open(path_raw_ground_truth,'w') as json_file:
            json.dump(data,json_file)
    else:
        logging.warning("%s not found"%path_raw_ground_truth)

def update_ids_all_ontologies():
    setup_logging_new_ids()
    ontologies= get_topic_ontologies()
    #ontologies.append('wikipedia-errors-and-missing')

    for ontology in ontologies:
        update_topic_ids_judgements_raw(ontology)


def merge_wikipedia_with_errors_and_missing_raw():
    annotator_map=get_annotator_map()
    annotator=annotator_map['wikipedia']
    setup_logging_merging_wikipedia_judgements()
    path_wikipedia_raw_ground_truth=get_path_ground_truth_raw('topic-matching','wikipedia')
    path_wikipedia_errors_and_missing_raw_ground_truth=get_path_ground_truth_raw('topic-matching','wikipedia-errors-and-missing')
    #path_wikipedia_raw_ground_truth_debug=path_wikipedia_raw_ground_truth.replace(".json",".debug.json")
    with open (path_wikipedia_raw_ground_truth) as wikipedia_json_file:
        data_wiki= json.load(wikipedia_json_file)
        documents_wiki=get_documents(data_wiki,annotator)
        logging.warning("count of documents in Wikipedia: %d"%(len(documents_wiki)))
        with open (path_wikipedia_errors_and_missing_raw_ground_truth) as wikipedia_erros_json_file:
            data_wiki_errors= json.load(wikipedia_erros_json_file)
            documents_errors=get_documents(data_wiki_errors,annotator)
            logging.warning("count of documents to update: %d"%(len(documents_errors)))
            for error_document in documents_errors:
                new_annotations=documents_errors[error_document]
                logging.warning("error document: "+error_document)
                if error_document in documents_wiki:
                    logging.warning("updating the document: "+error_document)
                    old_annotation=documents_wiki.pop(error_document)
                documents_wiki[error_document]=new_annotations
    with open(path_wikipedia_raw_ground_truth,'w') as wikipedia_new_json_file:
        json.dump(data_wiki,wikipedia_new_json_file)
    logging.warning(" saving %d documents to %s"%(len(documents_wiki),path_wikipedia_raw_ground_truth))


def merge_new_topics_all_ontologies():
    for ontology in get_topic_ontologies():
        path_raw_ground_truth_new= get_path_ground_truth_raw_new('topic-matching',ontology)
        if os.path.exists(path_raw_ground_truth_new):
            merge_new_topics(ontology)

def merge_new_topics(ontology):
    print(ontology)
    annotator_map=get_annotator_map()
    annotator=annotator_map[ontology]
    path_raw_ground_truth=get_path_ground_truth_raw('topic-matching',ontology)
    path_raw_ground_truth_new= get_path_ground_truth_raw_new('topic-matching',ontology)
    with open (path_raw_ground_truth) as json_file:
        data= json.load(json_file)
        documents=get_documents(data,annotator)
        with open(path_raw_ground_truth_new) as json_file_new:
            data_new = json.load(json_file_new)
            new_documents=get_documents(data_new,annotator)
            for document in new_documents:
                if document not in documents:
                    documents[document]=new_documents[document]


    with open(path_raw_ground_truth,'w') as json_file:
        json.dump(data,json_file)


if __name__ == "__main__":
    update_ids_all_ontologies()