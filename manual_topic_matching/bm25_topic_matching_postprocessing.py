import pandas as pd
from conf.configuration import *
from preprocessing.topic_inventory_postprocessing import *
import logging
def setup_logging_new_ids():
    logging.basicConfig(format="%(message)s",filename="../logs/search-new-ids.log",level=logging.DEBUG)
    logging.warning(datetime.now())
def update_no_matches(ontology):
    path_no_matches=get_path_judgements_model('topic-matching',ontology+"-no-matches")
    #path_no_matches_debug=path_no_matches.replace(".csv",".debug.csv")
    df_no_matches=pd.read_csv(path_no_matches,sep=",",encoding="utf-8")
    id_map=load_new_topic_id_map()
    logging.warning("updating ids for %s"%ontology)
    counter=0
    for index,no_match_record in df_no_matches.iterrows():
        counter=counter + 1
        old_id=no_match_record['id']
        new_id=id_map[old_id]
        df_no_matches.loc[index,'id']=new_id
        logging.warning("changing topic id from %d to %d"%(old_id,new_id))
    logging.warning("updated %d records in %s"%(counter,path_no_matches))
    df_no_matches.to_csv(path_no_matches,sep=",",encoding="utf-8",index=False)
def update_no_matches_all_ontologies():
    setup_logging_new_ids()
    ontologies=get_topic_ontologies()
    #ontologies.append('wikipedia-errors-and-missing')
    for ontology in ontologies:
        update_no_matches(ontology)


