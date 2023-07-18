import pandas as pd
import csv
from cassis import *
from conf.configuration import *
import re
from utils import *
def load_type_system():
    path_type_system = get_path_source_part("ukp-user-generated-web-discourse", "typesystem")
    with open(path_type_system , 'rb') as f:
        type_system = load_typesystem(f)
    return type_system

def parse_file(path,type_system):
    topic=None
    with open(path, 'rb') as f:
        cas = load_cas_from_xmi(f, typesystem=type_system)
        for meta_data in cas.select('de.tudarmstadt.ukp.dkpro.argumentation.types.WebArgumentMetadata'):
            topic=meta_data.topic
    return cas.sofa_string.replace("\t","").replace("\n",""), topic

def preprocess_topics(df_topics):
    df_topics['topic']=df_topics.apply(lambda x: x['topic'].replace("versus",""),axis=1)
    df_topics['topic']=df_topics.apply(lambda x: x['topic'].replace("vs mixed-sex education",""),axis=1)
    df_topics['topic']=df_topics.apply(lambda x: x['topic'].strip(),axis=1)
    df_topics['topic']=df_topics.apply(lambda x: re.sub("\s+"," ",x['topic']),axis=1)
    print(df_topics)
    return df_topics
def preprocess():
    corpus_path = get_path_source_part("ukp-user-generated-web-discourse", "arguments")
    path_preprocessed_documents = get_path_preprocessed_documents("ukp-user-generated-web-discourse")
    path_topics_web_discourse=get_path_preprocessed_topics('ukp-user-generated-web-discourse')
    path_document_topic=get_path_document_topic('ukp-user-generated-web-discourse')
    df_topics = pd.read_csv(path_topics_web_discourse,sep=",",encoding="utf-8")
    df_topics=preprocess_topics(df_topics)
    file_system = load_type_system()
    ids= []
    documents = []
    topics=[]
    for root,dirs,files in os.walk(corpus_path):
        for file_name in files:
            if file_name.endswith(".xmi"):
                path_file= os.path.join(root,file_name)
                document, topic= parse_file(path_file,file_system)
                documents.append(document)
                ids.append(file_name.replace(".xmi",""))
                topics.append(topic)
                print(topic)
    web_discourse_df= pd.DataFrame({"document-id":ids,"document":documents,'topic':topics})
    web_discourse_df['document']=web_discourse_df.apply((lambda row: drop_separator(row['document'],"\",\"")),axis=1)
    web_discourse_df.to_csv(path_preprocessed_documents,quotechar='"',sep=",",quoting=csv.QUOTE_ALL,encoding="utf-8",
                            columns=['document-id','document'],index=False)

    web_discourse_df['topic']=web_discourse_df.apply(lambda row:row['topic'].replace("-"," ") if (not 'single-sex' in row['topic'] ) else row['topic'].replace("sex-education","sex education"),axis=1)
    web_discourse_df=web_discourse_df.merge(df_topics,on="topic")
    web_discourse_df.to_csv(path_document_topic,quotechar='"',sep=",",quoting=csv.QUOTE_ALL,encoding="utf-8",
                            columns=['document-id','topic-id'],index=False)

preprocess()