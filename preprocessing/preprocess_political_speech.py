import pandas as pd
from conf.configuration import *

import csv
from utils import *
def preproces_corpus():
    speakers=['clegg','miliband','cameron']
    path_preprocessed_arguments = get_path_preprocessed_arguments('political-speech')
    path_preprocessed_documents = get_path_preprocessed_documents('political-speech')
    ids=[]
    arguments=[]
    document_ids=[]
    documents=[]
    for speaker in speakers:
        document_ids.append(speaker)
        path_speaker=get_path_source_part('political-speech', speaker)
        path_speaker_labels=get_path_source_part('political-speech', speaker + '-labels')
        sentences=[]
        speaker_ids=[]
        for line  in open(path_speaker,'r').readlines():
            sentence=line[line.index(' '):]
            sentences.append(sentence.strip())
            id=line[:line.index(' ')]
            speaker_id = speaker+'-'+id
            speaker_ids.append(speaker_id)
        documents.append("".join(sentences))
        speaker_labels=map(lambda label:label.replace('\n',''),open(path_speaker_labels,'r').readlines())
        sentences_with_labels = list(zip(speaker_ids,sentences,speaker_labels))
        speaker_claims_tuples = filter(lambda sentence_label_tuple: sentence_label_tuple[2] == 'C', sentences_with_labels)
        speaker_claim_ids = [sentence_label_pair[0] for sentence_label_pair in speaker_claims_tuples]
        speaker_claims_tuples = filter(lambda sentence_label_tuple: sentence_label_tuple[2] == 'C', sentences_with_labels)
        speaker_claims = [sentence_label_pair[1] for sentence_label_pair in speaker_claims_tuples]
        arguments.extend(speaker_claims)
        ids.extend(speaker_claim_ids)
    df_political_speeches_documents=pd.DataFrame({'document':documents,'document-id':document_ids})
    df_political_speeches_documents['document']=df_political_speeches_documents.apply((lambda row: drop_separator(row['document'],"\",\"")),axis=1)
    df_political_speeches_documents.to_csv(path_preprocessed_documents,quotechar='"',sep=",",columns=['document-id','document'],quoting=csv.QUOTE_ALL,encoding="utf-8",index=False)

    df_political_speeches_arguments=pd.DataFrame({'argument':arguments,'argument-id':ids})
    df_political_speeches_arguments['argument']=df_political_speeches_arguments.apply((lambda row: drop_separator(row['argument'],"\",\"")),axis=1)
    df_political_speeches_arguments.to_csv(path_preprocessed_arguments,quotechar='"',sep=",",quoting=csv.QUOTE_ALL,columns=['argument-id','argument'],encoding="utf-8",index=False)


preproces_corpus()