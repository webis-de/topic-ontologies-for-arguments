import pandas as pd
from conf.configuration import *
import logging
import csv
import tqdm
from utils import *

def configure_loging():
    logging.basicConfig(filename='../logs/preprocessed_kialo.log',level=logging.DEBUG)

configure_loging()

def filter_empty_arguments():
    path_preprocessed_arguments_kialo_empty = get_path_preprocessed_arguments_version('kialo','empty')
    path_preprocessed_arguments_kialo_non_empty =  get_path_preprocessed_arguments('kialo')

    df_kialo = pd.read_csv(path_preprocessed_arguments_kialo_empty,quotechar='"',sep=",",quoting=csv.QUOTE_ALL,encoding="utf-8",dtype={"argument":object}).dropna()

    df_kialo['argument-stripped']=df_kialo.apply(lambda row:row['argument'].strip(),axis=1)
    del df_kialo['argument']
    df_kialo.rename(columns={'argument-stripped':'argument'},inplace=True)
    empty_arguments =df_kialo[df_kialo['argument']==""]
    logging.warning("found %d empty arguments"%empty_arguments.shape[0])
    df_kialo=df_kialo[df_kialo['argument']!=""]
    logging.warning("saving arguments to %s"%path_preprocessed_arguments_kialo_non_empty)

    df_kialo['argument']=df_kialo.apply((lambda row: drop_separator(row['argument'],"\",\"")),axis=1)
    df_kialo.to_csv(path_preprocessed_arguments_kialo_non_empty,quotechar='"',sep=",",quoting=csv.QUOTE_ALL,
                    columns=['argument-id','argument'],encoding="utf-8")

configure_loging()
filter_empty_arguments()