import pandas as pd
import csv

from sklearn.cluster.tests.test_k_means import true_labels

from conf.configuration import *
from collections import Counter
import numpy
import logging
from sklearn.metrics import f1_score,recall_score,precision_score
from nltk.metrics.agreement import AnnotationTask
from automatic_topic_matching_evaluation.kappa import fleiss_kappa
import random
logging.basicConfig(filename="../logs/experiment-evaluation-agreement")
def read_judgements():
    path_judgements= get_path_judgement('topic-modeling-experiment')
    print(path_judgements)
    df=pd.read_csv(path_judgements,sep=",",encoding="utf-8",dtype={'topic.id':object})
    print(df.info())
    return df

def generate_majority_judgements():
    path_judgements_majority=get_path_judgements_majority('topic-modeling-experiment')
    def get_majority_label(row):
        c=Counter([row['annotator1'],row['annotator2'],row['annotator3']])
        return c.most_common(1)[0][0]
    df_judgements=read_judgements()
    df_judgements['label']=df_judgements.apply(get_majority_label,axis=1)
    df_judgements.to_csv(path_judgements_majority,sep=",",encoding='utf-8',index=False)

def read_judgements_majority(experiment):
    path_judgements_majority=get_path_judgements_majority('topic-modeling-experiment')


    df_judgements=pd.read_csv(path_judgements_majority,sep=",",dtype={'topic.id':object},encoding="utf-8")
    if 'debatepedia' in experiment:
        df_judgements= df_judgements[df_judgements['topic.id'].str.match("2.")]
    elif 'wikipedia-categories' in experiment:
        df_judgements= df_judgements[df_judgements['topic.id'].str.match("5.")]
    elif 'wikipedia' in experiment:
        df_judgements= df_judgements[df_judgements['topic.id'].str.match("3.")]
    elif 'strategic-intelligence-sub-topics' in experiment:
        df_judgements=df_judgements[df_judgements['topic.id'].str.match("4.")]
    elif 'strategic-intelligence' in experiment:
        df_judgements=df_judgements[df_judgements['topic.id'].str.match("1.")]
    else:
        None

    return df_judgements

def get_thresholds():
    return numpy.arange(0,1,0.01)

def generate_labels_threshold(experiment):
    logging.basicConfig(filename="../logs/labels-at-threshold.log",level=logging.DEBUG)
    models = get_models()
    thresholds= get_thresholds()
    df_judgements=read_judgements_majority(experiment)
    label_score_template="%s.score"

    for model in models:
        logging.warning("producing labels for model %s"%model)

        threshold_dfs=[]
        label_score=label_score_template%model
        for threshold in thresholds:
            logging.warning("producing labels for threshold %f"%threshold)
            df_judgements=df_judgements.copy()
            df_judgements['label.predicted']=df_judgements.apply(lambda row:row[label_score]>=threshold,axis=1)

            logging.warning("Count of all labels %d"%df_judgements.shape[0])
            logging.warning("Count of true labels %d"%df_judgements[df_judgements['label.predicted']].shape[0])

            df_judgements['threshold']=df_judgements.apply(lambda row:threshold,axis=1)

            df_threshold_judgements=df_judgements[['topic.id','document.id',label_score,'threshold','label.predicted','label']]
            threshold_dfs.append(df_threshold_judgements)

        df_labels_model_at_threshold=pd.concat(threshold_dfs)

        path_labels_model=get_path_labels_model_at_threshold(experiment,model)
        df_labels_model_at_threshold.to_csv(path_labels_model,sep=",",encoding="utf-8",index=False)
        logging.warning("saving labels for %s here %s"%(model,path_labels_model))

def generate_labels_top(experiment):
    logging.basicConfig(filename="../logs/labels-top-1.log",level=logging.DEBUG)
    models = get_models()
    df_judgements=read_judgements_majority(experiment)
    label_score_template="%s.score"
    for model in models:
        label_score=label_score_template%model
        logging.warning("producing labels for model %s"%model)
        topic_ids=[]
        scores=[]
        labels=[]
        labels_predicted=[]
        document_ids=[]
        for document_id, document_judgements in df_judgements.groupby('document.id'):
            max_score=document_judgements[label_score].max()
            topic_id=document_judgements['topic.id'].loc[document_judgements[label_score].idxmax()]
            label=document_judgements['label'].loc[document_judgements[label_score].idxmax()]
            scores.append(max_score)
            topic_ids.append(topic_id)
            labels.append(label)
            labels_predicted.append(True)
            document_ids.append(document_id)
        df_label_model_top_1=pd.DataFrame({'score':scores,'topic.id':topic_ids,'label.predicted':labels_predicted,'document.id':document_ids,'label':labels},columns=['topic.id','document.id','score','label.predicted','label'])
        path_labels_model_top_1=get_path_labels_model_top_1(experiment,model)
        df_label_model_top_1.to_csv(path_labels_model_top_1,sep=",",encoding="utf-8",index=False)
        logging.warning("saving labels for %s here %s"%(model,path_labels_model_top_1))

def calculate_agreement():
    topic_ontologies=get_topic_ontologies()
    kappas=[]
    alphas=[]
    topic_ontologies.append("")
    logging.basicConfig(filename="../logs/experiment-evaluation-agreement.log",level=logging.DEBUG)
    for ontology in topic_ontologies:
        if ontology!="":
            ontology= '-'+ontology
        experiment='topic-modeling-experiment'+ontology
        logging.warning("calcuating agreement for %s"%experiment)
        df_judgements=read_judgements_majority(experiment)
        annotations=[]
        fleiss_annotations=[]
        logging.warning("%d annotations will be analzyed"%df_judgements.shape[0])
        for index,row in df_judgements.iterrows():
            document_id = row['topic.id'] + "-"+ row['document.id']
            for annotator_id in range(1,4):
                annotator="annotator%d"%annotator_id
                annotator_label=row[annotator]
                annotations.append([annotator,document_id,annotator_label])
                fleiss_annotations.append((document_id,annotator_label))
        logging.warning("sample of the annotations: %s"%str(annotations[random.randint(0,len(annotations))]))
        logging.warning("sample of the fleiss annotations: %s"%str(fleiss_annotations[random.randint(0,len(fleiss_annotations))]))
        t= AnnotationTask(annotations)
        alpha = t.alpha()
        alphas.append(alpha)
        f_kappa= fleiss_kappa(fleiss_annotations,3,2)
        kappas.append(f_kappa)
    path_agreement =get_path_agreement('topic-modeling-experiment')
    df=pd.DataFrame({"ontology":topic_ontologies,'alpha':alphas,'kappas':kappas})
    df.to_csv(path_agreement)


def evaluate_models_thresholds(experiment):
    models = get_models()
    for model in models:
        path_labels_model=get_path_labels_model_at_threshold(experiment,model)
        df_labels_at_threshold=pd.read_csv(path_labels_model,dtype={'topic.id':object},sep=",",encoding="utf-8")
        labels_per_threshold = df_labels_at_threshold.sort_values('threshold').groupby('threshold')
        f1_scores=[]
        recalls=[]
        precisions=[]
        true_f1_scores=[]
        true_precisions=[]
        true_recalls=[]

        thresholds=[]
        for threshold, df_threshold_labels in labels_per_threshold:

            true_labels = df_threshold_labels['label'].values
            predicted_labels=df_threshold_labels['label.predicted'].values
            f1=f1_score(true_labels,predicted_labels,average='macro')
            recall=recall_score(true_labels,predicted_labels,average='macro')
            precision=precision_score(true_labels,predicted_labels,average='macro')

            thresholds.append(threshold)
            f1_scores.append(f1)
            recalls.append(recall)
            precisions.append(precision)

            true_f1= f1_score(true_labels,predicted_labels,average="binary",pos_label=True)
            true_recall=recall_score(true_labels,predicted_labels,average="binary",pos_label=True)
            true_precision=precision_score(true_labels,predicted_labels,average="binary",pos_label=True)

            true_f1_scores.append(true_f1)
            true_recalls.append(true_recall)
            true_precisions.append(true_precision)

        path_model_evaluation=get_path_evaluation_model(experiment,model)
        df_model_evaluation=pd.DataFrame({'true-f1-score':true_f1_scores,'true-recall':true_recalls,'true-precision':true_precisions,
                                          'f1-score':f1_scores,'recall':recalls,'precision':precisions,'threshold':thresholds})
        df_model_evaluation.to_csv(path_model_evaluation,sep=",",encoding="utf-8")




def evaluate_all_models(experiment):
    df_judgements_majority=read_judgements_majority(experiment)

    models=get_models()
    best_thresholds=[]
    f1_scores=[]
    precisions=[]
    recalls=[]
    true_f1_scores=[]
    true_precisions=[]
    true_recalls=[]

    f1_scores_at_one=[]
    precisions_at_one=[]
    recalls_at_one=[]
    for model in models:
        path_model_evaluation=get_path_evaluation_model(experiment,model)
        df_model_evaluation=pd.read_csv(path_model_evaluation,sep=",",encoding='utf-8')
        true_f1=df_model_evaluation['true-f1-score'].max()
        true_precision=df_model_evaluation['true-precision'].loc[df_model_evaluation['true-f1-score'].idxmax()]
        true_recall=df_model_evaluation['true-recall'].loc[df_model_evaluation['true-f1-score'].idxmax()]
        best_threshold=df_model_evaluation['threshold'].loc[df_model_evaluation['true-f1-score'].idxmax()]
        precision=df_model_evaluation['precision'].loc[df_model_evaluation['true-f1-score'].idxmax()]
        recall=df_model_evaluation['recall'].loc[df_model_evaluation['true-f1-score'].idxmax()]
        f1=df_model_evaluation['f1-score'].loc[df_model_evaluation['true-f1-score'].idxmax()]

        f1_scores.append(f1)
        precisions.append(precision)
        recalls.append(recall)
        best_thresholds.append(best_threshold)

        true_f1_scores.append(true_f1)
        true_precisions.append(true_precision)
        true_recalls.append(true_recall)
        
        path_labels_model_top_1=get_path_labels_model_top_1(experiment,model)
        df_model_top1_labels = pd.read_csv(path_labels_model_top_1,dtype={'topic.id':object},sep=",",encoding="utf-8")
        true_labels = df_model_top1_labels['label'].values
        predicted_labels=df_model_top1_labels['label.predicted'].values

        true_positives_at_1= [true_label and predicted_label for true_label,predicted_label in zip(true_labels,predicted_labels)]
        true_positives_at_1_count =Counter(true_positives_at_1).most_common(True)[0][1]



        all_positives=df_judgements_majority[df_judgements_majority['label']==True].shape[0]
        recall_at_one=float(true_positives_at_1_count)/all_positives

        precision_at_one=precision_score(true_labels,predicted_labels,average='binary',pos_label=True)
        f1_at_one = recall_at_one * precision_at_one*2/(precision_at_one+recall_at_one)
        f1_scores_at_one.append(f1_at_one)
        recalls_at_one.append(recall_at_one)
        precisions_at_one.append(precision_at_one)

    df_evaluation=pd.DataFrame({'threshold':best_thresholds,'model':models,'f1-score':f1_scores,'recall':recalls,'precision':precisions,
                                'true-f1-score':true_f1_scores,'true-recall':true_recalls,'true-precision':true_precisions,
                                'f1-score@1':f1_scores_at_one,'precision@1':precisions_at_one,'recall@1':recalls_at_one})

    path_evaluation=get_path_evaluation(experiment)
    df_evaluation.to_csv(path_evaluation,encoding="utf-8",sep=",",columns=['model','threshold','true-precision','true-recall','true-f1-score'])

calculate_agreement()



# generate_majority_judgements()
# generate_labels_top('topic-modeling-experiment')
# generate_labels_threshold('topic-modeling-experiment')
# evaluate_models_thresholds('topic-modeling-experiment')
# evaluate_all_models('topic-modeling-experiment')
#
#
# generate_labels_top('topic-modeling-experiment-wikipedia')
# generate_labels_threshold('topic-modeling-experiment-wikipedia')
# evaluate_models_thresholds('topic-modeling-experiment-wikipedia')
# evaluate_all_models('topic-modeling-experiment-wikipedia')
#
# generate_labels_top('topic-modeling-experiment-debatepedia')
# generate_labels_threshold('topic-modeling-experiment-debatepedia')
# evaluate_models_thresholds('topic-modeling-experiment-debatepedia')
# evaluate_all_models('topic-modeling-experiment-debatepedia')
#
# generate_labels_top('topic-modeling-experiment-wikipedia-categories')
# generate_labels_threshold('topic-modeling-experiment-wikipedia-categories')
# evaluate_models_thresholds('topic-modeling-experiment-wikipedia-categories')
# evaluate_all_models('topic-modeling-experiment-wikipedia-categories')
#
# generate_labels_top('topic-modeling-experiment-strategic-intelligence')
# generate_labels_threshold('topic-modeling-experiment-strategic-intelligence')
# evaluate_models_thresholds('topic-modeling-experiment-strategic-intelligence')
# evaluate_all_models('topic-modeling-experiment-strategic-intelligence')
#
# generate_labels_top('topic-modeling-experiment-strategic-intelligence-sub-topics')
# generate_labels_threshold('topic-modeling-experiment-strategic-intelligence-sub-topics')
# evaluate_models_thresholds('topic-modeling-experiment-strategic-intelligence-sub-topics')
# evaluate_all_models('topic-modeling-experiment-strategic-intelligence-sub-topics')

#read_judgements()