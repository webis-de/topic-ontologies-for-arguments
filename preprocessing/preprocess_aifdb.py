import pandas as pd
from conf.configuration import *
from langdetect import detect
import logging
import csv
import tqdm
logging_path="../logs/preprocessed_aifdb.log"
from utils import *
def set_logging_path():
    global logging_path
    logging.basicConfig(filename=logging_path,level=logging.DEBUG)
set_logging_path()
def filter_non_english_arguments():
    path_arguments_non_english = get_path_preprocessed_arguments_version("aifdb","non-english")
    logging.warning("argument path is %s" %path_arguments_non_english)
    path_arguments_english = get_path_preprocessed_arguments("aifdb")

    df=pd.read_csv(path_arguments_non_english,quotechar='"',sep="|",quoting=csv.QUOTE_ALL,encoding="utf-8").dropna()
    logging.info("Got %s rows"%str(df.shape[0]))
    df['argument_stripped']=df.apply(lambda row: row['argument'].strip().replace("\n","").replace("\t",""),axis=1)
    del df['argument']
    df.rename(columns={'argument_stripped':'argument'},inplace=True)
    df=df.loc[df['argument']!=""]
    logging.info("Got %d rows after deleting empty strings"%df.shape[0])
    df['language']=["" for index in df.index]
    df['is_english']=[False for index in df.index]
    indices_to_include=[]
    for index,row in tqdm.tqdm(df.iterrows()):
        try:

            language=detect(row['argument'])
            df.loc[index,'language']=language
            df.loc[index,'is_english']=language == 'en'
            indices_to_include.append(index)
        except:
            logging.error(row['argument'])
    df=df.loc[indices_to_include]
    df=df.loc[df['is_english']==True]
    logging.info("Got %d rows after non english arguments"%df.shape[0])
    hist = df['language'].value_counts()
    del df['language']
    del df['is_english']
    print(hist.to_string())
    df['argument']=df.apply((lambda row: drop_separator(row['argument'],"\",\"")),axis=1)
    df.to_csv(path_arguments_english,quotechar='"',sep=",",quoting=csv.QUOTE_ALL,columns=['argument-id','argument'],encoding="utf-8")

filter_non_english_arguments()