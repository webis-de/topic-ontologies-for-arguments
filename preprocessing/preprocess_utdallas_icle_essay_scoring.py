from conf.configuration import *
import pandas as pd
import csv
import cassis
from utils import *
def load_typesystem():
    path_type_system=get_path_source_part('utdallas-icle-essay-scoring', 'typesystem')
    with open(path_type_system , 'rb') as f:
        type_system = cassis.load_typesystem(f)
    return type_system

def load_cas(file_path,type_system):
    with open(file_path, 'rb') as f:
        cas = cassis.load_cas_from_xmi(f, typesystem=type_system)
    return cas

def extract_topic (cas):
   metadata=list(cas.select('de.aitools.ie.uima.type.argumentation.MetadataICLE'))
   return metadata[0].title

def extract_raw_document(document_name, filename_document_map):
    filename= document_name.replace(".xmi","")
    return filename_document_map[filename]
def read_file(file_path,encoding):
    file = open(file_path,'r',encoding=encoding,errors="ignore")
    header_skipped= False
    lines =[]
    for line in file:
        if not header_skipped:
            header_skipped = True
            continue
        cleaned_line = line
        lines.append(cleaned_line)
    content= " ".join(lines)
    content=content.replace("\n"," ").replace("\t"," ")
    return content

def get_annotated_aritcles():
    path_annotation_articles = get_path_source('utdallas-icle-essay-scoring')
    annotated_articles=[]
    annotated_aritcle_pathes=[]
    for root,dirs,files in os.walk(path_annotation_articles):
        for file in files:
            annotated_article=file.replace(".xmi","")
            annotated_articles.append(annotated_article)
            annotated_aritcle_pathes.append(os.path.join(root,file))
    return annotated_articles,annotated_aritcle_pathes

def preprocess_part(encoding):
    path_corpus_ascii = get_path_source_part("utdallas-icle-essay-scoring", encoding)
    for root,dirs,files in os.walk(path_corpus_ascii):
        documents = []
        for file_name in files:
            file_path = os.path.join(root,file_name)
            if encoding == 'iso-8859':
                python_encoding='latin_1'
            elif encoding == 'unknown-8bit':
                python_encoding='utf-8'
            else:
                python_encoding='ascii'
            file_content = read_file(file_path,python_encoding)
            documents.append(file_content)
    return documents,files


def preprocess():
    type_system=load_typesystem()
    encodings=  ['ascii','iso-8859','unknown-8bit']
    all_documents= []
    all_filenames=[]
    for encoding in encodings:
        documents,filenames = preprocess_part(encoding)
        filenames=[filename.replace(".txt","") for filename in filenames]
        all_documents.extend(documents)
        all_filenames.extend(filenames)

    filename_document_map = dict(zip(all_filenames,all_documents))
    path_preprocessed_topics=get_path_preprocessed_topics("utdallas-icle-essay-scoring")
    path_preprocessed_documents = get_path_preprocessed_documents("utdallas-icle-essay-scoring")
    path_document_topic=get_path_document_topic('utdallas-icle-essay-scoring')
    all_documents=[]
    all_ids = []
    all_topics = []
    annotated_documents,annotated_document_pathes = get_annotated_aritcles()
    for i,annotated_document in enumerate(annotated_documents):
        path_annotated_article=annotated_document_pathes[i]
        article_cas=load_cas(path_annotated_article,type_system)
        document= extract_raw_document(annotated_document,filename_document_map)
        topic= extract_topic(article_cas)
        all_topics.append(topic)
        all_documents.append(document)
        all_ids.append(annotated_document)
    unique_topics=list(set(all_topics))
    df_topics=pd.DataFrame({'topic':unique_topics,'topic-id':range(0,len(unique_topics))})
    df_topics.to_csv(path_preprocessed_topics,sep=",",columns=['topic-id','topic'],encoding="utf-8")

    all_ids=list(map(lambda x:x.replace(".txt",""),all_ids))
    df_dataset=pd.DataFrame({'topic':all_topics,'document':all_documents,'document-id':all_ids})
    df_dataset['document']=df_dataset.apply((lambda row: drop_separator(row['document'],"\",\"")),axis=1)
    df_dataset.to_csv(path_preprocessed_documents,quotechar='"',sep=",",quoting=csv.QUOTE_ALL,encoding="utf-8", \
                      columns=['document-id','document'],index=False)

    df_dataset=df_dataset.merge(df_topics,on='topic')
    df_dataset.to_csv(path_document_topic,quotechar='"',sep=",",quoting=csv.QUOTE_ALL,encoding="utf-8", \
                      columns=['document-id','topic-id'],index=False)
preprocess()