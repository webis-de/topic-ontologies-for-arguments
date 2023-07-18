from conf.configuration import *
import pandas as pd
from preprocessing.utils import *
import os
def preprocess():
    topics_map = {"AB.csv": "abortion", "DP.csv" : "death penalty", "MW.csv" : "minimum wage", "NP.csv": "nuclear power",
              "SU.csv": "school uniforms", "GC.csv": "gun control"}
    dataset = "basn"
    path_input = get_path_source_part(dataset,"input")
    path_output = get_path_source_part(dataset,"output")
    all_docs_ids = []
    all_documents = []
    all_topics = []
    unique_topics = topics_map.values()
    unique_topic_ids = range(0, len(unique_topics))
    path_topics = get_path_topics(dataset)
    df_topics = pd.DataFrame({"topic-id":unique_topic_ids, "topic":unique_topics})
    save_topics(df_topics,path_topics)
    print(path_input)
    for file in os.listdir(path_input):
        if file.endswith(".csv"):
            print(file)
            topic = topics_map[file]
            path_input_file = os.path.join(path_input, file)
            df_input = pd.read_csv(path_input_file, sep=",")
            df_input["doc"] = df_input.apply(lambda record: record["conclusion"] + " " + record["premises" ], axis=1)
            df_input["id"] = df_input.apply(lambda record: record["fragment_id"] +f"_arg_{topic}", axis = 1)
            topics = [topic for _ in df_input["doc"]]
            all_topics.extend(topics)
            all_docs_ids.extend(df_input["id"])
            all_documents.extend(df_input["doc"])
            path_output_file = os.path.join(path_output, file)
            df_output = pd.read_csv(path_output_file, sep=",")
            all_documents.extend(df_output["response"])
            df_output["id"] = df_output.apply(lambda record: record["fragment_id"] + "_" + str(record["response_no"]), axis=1)
            all_docs_ids.extend(df_output["id"])
            topics = [topic for _ in df_output["id"]]
            all_topics.extend(topics)

    df = pd.DataFrame({"document":all_documents, "document-id":all_docs_ids, "topic":all_topics})
    clean_documents(df)
    df_doc_topics = df.merge(df_topics, on="topic")
    path_topics = get_path_preprocessed_topics(dataset)
    path_docs = get_path_preprocessed_documents(dataset)
    path_document_topics = get_path_document_topic(dataset)
    save_topics(df_topics, path_topics)
    save_documents(df, path_docs)
    save_document_topic(df_doc_topics, path_document_topics)

preprocess()