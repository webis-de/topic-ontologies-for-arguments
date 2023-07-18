from conf.configuration import *
import pandas as pd
import csv
path= get_path_preprocessed_documents('sample')
path_html= path.replace('csv','html')
df=pd.read_csv(path,quotechar='"',sep=",",quoting=csv.QUOTE_ALL,encoding="utf-8")
df.to_html(path_html,encoding="utf-8")