from conf.configuration import *
import pandas as pd
import csv
from utils import *
def preprocess_subset(part):
    path_subset = get_path_source_part('ibm-debater-claim-sentence-search', part)
    df = pd.read_csv(path_subset,sep=",",encoding="utf-8")
    sentences = zip(list(df['sentence']),list(df['mc']))


    return sentences

def extract_topics(part):
    path_subset = get_path_source_part('ibm-debater-claim-sentence-search', part)
    df = pd.read_csv(path_subset,sep=",",encoding="utf-8",columns={'topic-id','topic'})
    df=df.drop_duplicates('mc')
    return df.mc
def preprocess():
    path_preprocessed_documents = get_path_preprocessed_documents("ibm-debater-claim-sentence-search")
    path_preprocessed_topics = get_path_preprocessed_topics("ibm-debater-claim-sentence-search")
    path_document_topics=get_path_document_topic('ibm-debater-claim-sentence-search')
    documents=[]

    training_pairs= preprocess_subset('training')
    test_pairs = preprocess_subset('test')
    heldout_pairs = preprocess_subset('heldout')



    documents_training, topics_training=zip(*training_pairs)
    documents_test, topics_test=zip(*test_pairs)
    documents_heldout, topics_heldout=zip(*heldout_pairs)
    topics=[]

    topics.extend(topics_training)
    topics.extend(topics_test)
    topics.extend(topics_heldout)

    unique_topics=[]
    for topic in topics:
        if topic not in unique_topics:
            unique_topics.append(topic)
    unique_topic_ids= range(0,len(unique_topics))

    df_topics= pd.DataFrame({"topic":unique_topics,"topic-id":unique_topic_ids})
    df_topics.to_csv(path_preprocessed_topics,sep=",",encoding="utf-8",index=False)



    topics_ids_map={unique_topic:unique_topic_id for (unique_topic,unique_topic_id) in zip(unique_topics,unique_topic_ids)}

    topic_ids = [topics_ids_map[topic] for topic in topics]

    documents.extend(documents_training)
    documents.extend(documents_test)
    documents.extend(documents_heldout)
    all_ids = range(0,len(documents))

    df_documents = pd.DataFrame({"document":documents,"document-id":all_ids , 'topic-id':topic_ids})
    df_documents['document']=df_documents.apply((lambda row: drop_separator(row['document'],"\",\"")),axis=1)
    df_documents.to_csv(path_preprocessed_documents,quotechar='"',sep=",",quoting=csv.QUOTE_ALL,encoding="utf-8", \
                        columns=['document-id','document'],index=False)

    df_document_topics = pd.DataFrame({"document":documents,"document-id":all_ids , 'topic-id':topic_ids})
    df_document_topics.to_csv(path_document_topics,quotechar='"',sep=",",quoting=csv.QUOTE_ALL,encoding="utf-8", \
                      columns=['document-id','topic-id'],index=False)



preprocess()