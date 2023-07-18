import pandas as pd
import csv
from conf.configuration import *
from utils import *
def reformat(path_input,path_output):
    df = pd.read_csv(path_input,sep=",",quotechar='"',encoding='utf-8')
    if 'document' in df.columns:
        df['document']=df.apply((lambda row: drop_separator(row['document'],"\",\"")),axis=1)
    else:
        df['argument']=df.apply((lambda row: drop_separator(row['argument'],"\",\"")),axis=1)
    df.to_csv(path_output,quotechar='"',sep=",",quoting=csv.QUOTE_ALL,encoding="utf-8",index=False)

path_preprocessed_arguments_kialo= get_path_preprocessed_arguments('kialo')
path_preprocessed_documents_kialo= get_path_preprocessed_documents('kialo')
path_preprocessed_arguments_aifdb= get_path_preprocessed_arguments('aifdb')
path_preprocessed_documents_aifdb= get_path_preprocessed_documents('aifdb')
path_preprocessed_arguments_ukp_arguments_annotated_essays_v2= get_path_preprocessed_arguments('ukp-argument-annotated-essays-v2')
path_preprocessed_documents_ukp_documents_annotated_essays_v2= get_path_preprocessed_documents('ukp-argument-annotated-essays-v2')
path_preprocessed_arguments_upittsburg_arguments_subjectivity= get_path_preprocessed_arguments('upittsburgh-arguing-subjectivity')
path_preprocessed_documents_upittsburg_documents_subjectivity= get_path_preprocessed_documents('upittsburgh-arguing-subjectivity')
#reformat(path_preprocessed_arguments_ukp_arguments_annotated_essays_v2,path_preprocessed_arguments_ukp_arguments_annotated_essays_v2)
#reformat(path_preprocessed_documents_ukp_documents_annotated_essays_v2,path_preprocessed_documents_ukp_documents_annotated_essays_v2)
#reformat(path_preprocessed_arguments_kialo,path_preprocessed_arguments_kialo)
#reformat(path_preprocessed_documents_kialo,path_preprocessed_documents_kialo)
reformat(path_preprocessed_arguments_aifdb,path_preprocessed_arguments_aifdb)
#reformat(path_preprocessed_documents_aifdb,path_preprocessed_documents_aifdb)

# reformat(path_preprocessed_arguments_upittsburg_arguments_subjectivity,path_preprocessed_arguments_upittsburg_arguments_subjectivity)
# reformat(path_preprocessed_documents_upittsburg_documents_subjectivity,path_preprocessed_documents_upittsburg_documents_subjectivity)