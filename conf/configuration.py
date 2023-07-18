import os
import io
topic_coverage_document_label='topic-coverage-document'
topic_coverage_corpus_topic= 'topic-coverage-corpus-topic'
citing_papers_links_label='citing-papers-links'
citing_papers_text_label='citing-papers-text'
citing_papers_index_label='citing-papers-index'
citing_papers_label='citing-papers'
experiment_papers_label='experiment-papers'
source_label ="source"
sample_label ="sample"
part_count_label='part_count'
judgements_label="judgements"
judgements_model_label="judgements-%s"
evaluation_label="evaluation"
agreement_label="agreement"
ground_truth_corpora_label_template='ground-truth-corpora-%s'
ground_truth_label_template='ground-truth-%s'
ground_truth_raw_label_template='ground-truth-raw-%s'
ground_truth_raw_label_new_template='ground-truth-raw-%s-new'
source_label_template="source-%s"
preprocessed_documents_label = "preprocessed-documents"
preprocessed_topics_label = "preprocessed-topics"
preprocessed_arguments_label = "preprocessed-arguments"
preprocessed_arguments_version_label_template="preprocessed-arguments-%s"
preprocessed_documents_version_label_template= "preprocessed-documents-%s"
preprocessed_part_label_template="preprocessed-%s"
document_topic_label='document-topic'
document_topic_label_template='document-topic-%s'
argument_topic_label='argument-topic'
document_vectors_label_template="document-vectors-%s-%s"
document_vectors_part_label_template="document-vectors-%s-%s-part-%d"
argument_vectors_label_template="argument-vectors-%s-%s"
histogram_label_template= "%s_histogram_%s"
two_parameter_histogram_template= "histogram-%s-over-%s"
two_parameter_histogram_template_figure = "figure-histogram-%s-over-%s"
two_parameter_plot_template_figure = "figure-plot-%s-over-%s"
histogram_label_fig_template= "%s-histogram-%s-fig"
model_label_template="%s-model"
vocab_label_template="%s-vocab"
topics_label="topics"
granularity_label="granularity"
top_k_topics_per_document_label= "top-k-topics-per-document"
top_k_topics_per_argument_label= "top-k-topics-per-argument"
top_topics_per_document_label_threshold= "top-topics-per-document-threshold"
top_topics_per_argument_label_threshold= "top-topics-per-argument-threshold"
best_topics_per_document_label_template="best-topics-per-dcoument-%s"
all_topics_per_document_label= "all-topics-per-document"
dirname = os.path.dirname(__file__)
cluster_mode=False
cluster_conf_path="hdfs://nn.hdfs.webis.de:8020/user/befi8957/topic-ontologies/conf/"
windows_mode=False
hashmap_label_template='hashmap-%s-%s'
labels_model_at_threshold= "labels-model-at-threshold"
labels_model_top_1= "labels-model-top-1"
evaluation_model= "evaluation-model"
judgements_majority="judgements-majority"
documents_label_template="documents-%s"
import zipfile
def get_dataset_conf_path(dataset_name):
    if cluster_mode:
        return dataset_name
    else:

        dataset_conf = dirname+("/%s.conf"%dataset_name)
    return dataset_conf

def get_path_source(dataset_name):
    dataset_conf_path = get_dataset_conf_path(dataset_name)
    dataset_source_path = get_property_value(dataset_conf_path,source_label)
    return dataset_source_path

def get_path_ground_truth(dataset_name,ontology):
    dataset_conf_path = get_dataset_conf_path(dataset_name)
    ground_truth_label=ground_truth_label_template%ontology
    return get_property_value(dataset_conf_path,ground_truth_label)

def get_path_ground_truth_corpora(dataset_name,ontology):
    dataset_conf_path = get_dataset_conf_path(dataset_name)
    ground_truth_corpora_label=ground_truth_corpora_label_template%ontology
    return get_property_value(dataset_conf_path,ground_truth_corpora_label)

def get_path_ground_truth_raw(dataset_name,ontology):
    dataset_conf_path = get_dataset_conf_path(dataset_name)
    ground_truth_label=ground_truth_raw_label_template%ontology
    return get_property_value(dataset_conf_path,ground_truth_label)

def get_path_ground_truth_raw_new(dataset_name,ontology):
    dataset_conf_path = get_dataset_conf_path(dataset_name)
    ground_truth_label=ground_truth_raw_label_new_template%ontology
    return get_property_value(dataset_conf_path,ground_truth_label)


def get_path_document_topic(dataset_name):
    dataset_conf_path = get_dataset_conf_path(dataset_name)
    path_document_topic=get_property_value(dataset_conf_path,document_topic_label)
    return path_document_topic

def get_path_document_topic_ontology(dataset_name,ontology):
    dataset_conf_path = get_dataset_conf_path(dataset_name)
    document_topic_label=document_topic_label_template%ontology
    path_document_topic=get_property_value(dataset_conf_path,document_topic_label)
    return path_document_topic

def get_path_argument_topic(dataset_name):
    dataset_conf_path = get_dataset_conf_path(dataset_name)
    path_argument_topic=get_property_value(dataset_conf_path,argument_topic_label)
    return path_argument_topic

def get_path_judgement(dataset_name):
    dataset_conf_path = get_dataset_conf_path(dataset_name)
    path_judgement= get_property_value(dataset_conf_path,judgements_label)
    return path_judgement

def get_path_judgements_model(dataset_name,model):
    dataset_conf_path = get_dataset_conf_path(dataset_name)
    judgements_label=judgements_model_label%model
    return get_property_value(dataset_conf_path,judgements_label)

def get_path_evaluation(dataset_name):
    dataset_conf_path = get_dataset_conf_path(dataset_name)
    path_evaluation= get_property_value(dataset_conf_path,evaluation_label)
    return path_evaluation

def get_path_source_part(dataset_name, subdataset):
    dataset_conf_path = get_dataset_conf_path(dataset_name)
    source_label = source_label_template % subdataset
    dataset_source_subset_path = get_property_value(dataset_conf_path,source_label)
    return dataset_source_subset_path

def get_sample_path(dataset_name):
    dataset_conf_path = get_dataset_conf_path(dataset_name)
    dataset_sample_path = get_property_value(dataset_conf_path,sample_label)
    return dataset_sample_path

def get_path_document_vectors(dataset_name,topic_ontology,topic_model):
    dataset_conf_path = get_dataset_conf_path(dataset_name)
    document_vectors_label = document_vectors_label_template % (topic_ontology, topic_model)
    return get_property_value(dataset_conf_path,document_vectors_label)

def get_path_document_vectors_part(dataset_name,topic_ontology,topic_model,part):
    dataset_conf_path = get_dataset_conf_path(dataset_name)
    document_vectors_label = document_vectors_part_label_template % (topic_ontology, topic_model,part)
    return get_property_value(dataset_conf_path,document_vectors_label)


def get_path_argument_vectors(dataset_name,topic_ontology,topic_model):
    dataset_conf_path = get_dataset_conf_path(dataset_name)
    argument_vectors_label = argument_vectors_label_template % (topic_ontology, topic_model)
    return get_property_value(dataset_conf_path,argument_vectors_label )

def get_path_vocab(dataset_name):
    dataset_conf_path = get_dataset_conf_path(dataset_name)
    vocab_label = vocab_label_template% dataset_name
    path_vocab = get_property_value(dataset_conf_path,vocab_label)
    return path_vocab

def get_path_hashmap(dataset_name,source,destination):
    path_dataset_conf=get_dataset_conf_path(dataset_name)
    label=hashmap_label_template%(source,destination)
    path_hashmap=get_property_value(path_dataset_conf,label)
    return path_hashmap

def get_path_preprocessed_documents(dataset_name):
    dataset_conf_path = get_dataset_conf_path(dataset_name)
    path_preprocessed_documents = get_property_value(dataset_conf_path,preprocessed_documents_label)
    return path_preprocessed_documents

def get_path_preprocessed_arguments(dataset_name):
    dataset_conf_path = get_dataset_conf_path(dataset_name)
    path_preprocessed_arguments = get_property_value(dataset_conf_path,preprocessed_arguments_label)
    return path_preprocessed_arguments

def get_path_preprocessed_topics(dataset_name):
    dataset_conf_path = get_dataset_conf_path(dataset_name)
    path_preprocessed_topics = get_property_value(dataset_conf_path,preprocessed_topics_label)
    return path_preprocessed_topics

def get_path_preprocessed_part(dataset_name,part):
    dataset_conf_path = get_dataset_conf_path(dataset_name)
    preprocessed_part_label= preprocessed_part_label_template %(part)
    return get_property_value(dataset_conf_path,preprocessed_part_label)

def get_path_preprocessed_arguments_version(dataset_name,version):
    dataset_conf_path = get_dataset_conf_path(dataset_name)
    preprocessed_arguments_version_label = preprocessed_arguments_version_label_template% version
    path_preprocessed_arguments_template = get_property_value(dataset_conf_path,preprocessed_arguments_version_label)
    return path_preprocessed_arguments_template

def get_path_preprocessed_documents_version(dataset_name,version):
    dataset_conf_path = get_dataset_conf_path(dataset_name)
    path_preprocessed_documents_label = preprocessed_documents_version_label_template%version
    path_preprocessed_documents = get_property_value(dataset_conf_path, path_preprocessed_documents_label)
    return path_preprocessed_documents

def get_histogram_path_figure(dataset_name,attribute):
    dataset_conf_path = get_dataset_conf_path(dataset_name)
    dataset_histogram_attribute_label = histogram_label_fig_template % (dataset_name, attribute)
    dataset_histogram_figure_attribute_path = get_property_value(dataset_conf_path,dataset_histogram_attribute_label)
    return dataset_histogram_figure_attribute_path

def get_path_histogram_two_parameters(dataset_name, x, y):
    dataset_conf_path = get_dataset_conf_path(dataset_name)
    dataset_histogram_label = two_parameter_histogram_template % ( x, y)
    dataset_histogram_path = get_property_value(dataset_conf_path,dataset_histogram_label)
    return dataset_histogram_path

def get_path_figure_histogram_two_parameters(dataset_name, x, y):
    dataset_conf_path = get_dataset_conf_path(dataset_name)
    dataset_histogram_label = two_parameter_histogram_template_figure % (x, y)
    dataset_histogram_figure_path = get_property_value(dataset_conf_path,dataset_histogram_label)
    return dataset_histogram_figure_path

def get_path_figure_plot_two_parameters(dataset_name,x,y):
    dataset_conf_path = get_dataset_conf_path(dataset_name)
    dataset_plot_label = two_parameter_plot_template_figure% (x, y)
    dataset_histogram_figure_path = get_property_value(dataset_conf_path,dataset_plot_label)
    return dataset_histogram_figure_path

def get_path_topic_coverage_document(dataset,ontology):
    dataset_conf_path = get_dataset_conf_path(dataset)
    path_topic_coverage=get_property_value(dataset_conf_path,topic_coverage_document_label)
    return path_topic_coverage%ontology

def get_path_topic_coverage_corpus_topic(dataset,ontology):
    dataset_conf_path = get_dataset_conf_path(dataset)
    path_topic_coverage=get_property_value(dataset_conf_path, topic_coverage_corpus_topic)
    return path_topic_coverage%ontology


def get_path_topics(ontology_name):
    dataset_conf_path = get_dataset_conf_path(ontology_name)
    path_topics = get_property_value(dataset_conf_path,'topics')
    return path_topics

def get_path_topic_model(ontology_name,model):
    dataset_conf_path = get_dataset_conf_path(ontology_name)
    model_label = model_label_template % model
    path_topic_model = get_property_value(dataset_conf_path,model_label)
    return path_topic_model

def get_histogram_path(dataset_name,attribute):
    dataset_conf_path = get_dataset_conf_path(dataset_name)
    dataset_histogram_attribute_label = histogram_label_template % (dataset_name, attribute)
    dataset_histogram_attribute_path = get_property_value(dataset_conf_path,dataset_histogram_attribute_label)
    return dataset_histogram_attribute_path

def get_path_top_k_topics_per_document(dataset,topic_ontology,topic_model,k):
    dataset_conf_path = get_dataset_conf_path(dataset)
    top_k_topics_per_document_path_template = get_property_value(dataset_conf_path,top_k_topics_per_document_label)
    top_k_topics_per_document_path=  top_k_topics_per_document_path_template % (k,topic_ontology, topic_model)
    return top_k_topics_per_document_path

def get_path_best_topics_per_document(dataset,topic_ontology):
    dataset_conf_path = get_dataset_conf_path(dataset)
    best_topics_per_document_label=best_topics_per_document_label_template%topic_ontology
    return get_property_value(dataset_conf_path,best_topics_per_document_label)
def get_path_all_topics_per_document(dataset,topic_ontology,topic_model):
    dataset_conf_path = get_dataset_conf_path(dataset)
    all_topics_per_document_path_template = get_property_value(dataset_conf_path,all_topics_per_document_label)
    all_topics_per_document_path=  all_topics_per_document_path_template % (topic_ontology, topic_model)
    return all_topics_per_document_path

def get_path_top_k_topics_per_argument(dataset,topic_ontology,topic_model,k):
    dataset_conf_path = get_dataset_conf_path(dataset)
    top_k_topics_per_argument_path_template = get_property_value(dataset_conf_path,top_k_topics_per_argument_label)
    top_k_topics_per_argument_path=  top_k_topics_per_argument_path_template % (k,topic_ontology, topic_model)
    return top_k_topics_per_argument_path

def get_path_topics_per_document_threshold(dataset,topic_ontology,topic_model,threshold):
    dataset_conf_path = get_dataset_conf_path(dataset)
    top_topics_per_document_path_template = get_property_value(dataset_conf_path,top_topics_per_document_label_threshold)
    path_top_topics_per_document= top_topics_per_document_path_template %(topic_ontology,topic_model,threshold)
    return path_top_topics_per_document

def get_path_topics_per_argument_threshold(dataset,topic_ontology,topic_model,threshold):
    dataset_conf_path = get_dataset_conf_path(dataset)
    path_top_topics_per_argument_threshold_template = get_property_value(dataset_conf_path,top_topics_per_argument_label_threshold)
    path_top_topics_per_argument_threshold= path_top_topics_per_argument_threshold_template %(topic_ontology,topic_model,threshold)
    return path_top_topics_per_argument_threshold

def get_path_citing_papers_links(dataset):
    dataset_conf_path = get_dataset_conf_path(dataset)
    path_citing_papers_links= get_property_value(dataset_conf_path,citing_papers_links_label)
    return path_citing_papers_links

def get_path_citing_papers(dataset):
    dataset_conf_path = get_dataset_conf_path(dataset)
    path_citing_papers= get_property_value(dataset_conf_path,citing_papers_label)
    return path_citing_papers

def get_path_citing_papers_text(dataset):
    dataset_conf_path = get_dataset_conf_path(dataset)
    path_citing_papers_text= get_property_value(dataset_conf_path,citing_papers_text_label)
    return path_citing_papers_text

def get_path_citing_papers_index(dataset):
    dataset_conf_path = get_dataset_conf_path(dataset)
    path_citing_papers_index= get_property_value(dataset_conf_path,citing_papers_index_label)
    return path_citing_papers_index

def get_path_experiment_papers(dataset):
    dataset_conf_path = get_dataset_conf_path(dataset)
    path_experiment_papers= get_property_value(dataset_conf_path,experiment_papers_label)
    return path_experiment_papers

def get_property_value(dataset_conf_path,property_label):
    if cluster_mode:
        with zipfile.ZipFile(dirname.replace("/conf","")) as myzip:
            conf_file=io.TextIOWrapper(myzip.open("conf/%s.conf"%dataset_conf_path,mode='r'))
    else:
        conf_file = open(dataset_conf_path,'r')


    for line in conf_file:
        label = line.split("=")[0].strip()
        value = line.split("=")[1].strip()
        root=get_root()
        if label == property_label:
            if value.startswith("/"):
                if value.startswith("/mnt") or value.startswith("/home") :
                    return value
                else:
                    return root+value
            else:
                return value

def get_topic_ontologies():
    #return ['debatepedia','strategic-intelligence-sub-topics']
    return ['strategic-intelligence']
    #return ['strategic-intelligence','wikipedia-categories','wikipedia']
    #return ['strategic-intelligence','strategic-intelligence-sub-topics','wikipedia-categories','wikipedia','debatepedia']

def get_granularity(dataset):
    dataset_conf_path = get_dataset_conf_path(dataset)
    granularity = get_property_value(dataset_conf_path,granularity_label)
    return granularity

def load_corpora_list(corpora_set=None):
    if corpora_set==None:
        corpora_path = get_dataset_conf_path('corpora')
    else:
        corpora_path =get_dataset_conf_path(corpora_set)
    with open(corpora_path,'r') as corpora_file:
        return [l.strip() for l in corpora_file.readlines()]

def load_cliches(cliches_set=None):
    if cliches_set==None:
        cliche_path=get_dataset_conf_path('cliches')
    with open(cliche_path,'r') as cliche_file:
        return [l.strip() for l in cliche_file.readlines()]

def get_models():
    return  ['direct-match','esa','esa-lemmatized','word2vec-esa-100','bert','weighted-bert','elmo','weighted-elmo',
              'flair','weighted-flair','glove','weighted-glove']

def get_path_labels_model_at_threshold(dataset,model):
    dataset_conf_path = get_dataset_conf_path(dataset)
    path_labels_model_at_threshold=get_property_value(dataset_conf_path,labels_model_at_threshold)
    return path_labels_model_at_threshold%model

def get_path_labels_model_top_1(dataset,model):
    dataset_conf_path = get_dataset_conf_path(dataset)
    path_labels_model_top_1_template=get_property_value(dataset_conf_path,labels_model_top_1)
    return path_labels_model_top_1_template%model

def get_path_evaluation_model(dataset,model):
    dataset_conf_path = get_dataset_conf_path(dataset)
    path_evaluation_model_template= get_property_value(dataset_conf_path, evaluation_model)
    return path_evaluation_model_template%model

def get_path_judgements_majority(dataset):
    dataset_conf_path = get_dataset_conf_path(dataset)
    path_judgements= get_property_value(dataset_conf_path,judgements_majority)
    return path_judgements

def get_path_agreement(dataset):
    dataset_conf_path = get_dataset_conf_path(dataset)
    path_agreement= get_property_value(dataset_conf_path,agreement_label)
    return path_agreement


def get_part_count(dataset):
    dataset_conf_path = get_dataset_conf_path(dataset)
    part_count= get_property_value(dataset_conf_path,part_count_label)
    if part_count!=None:
        return int(part_count)
    else:
        return part_count

def get_documents_path(dataset, version):
    path_dataset= get_dataset_conf_path(dataset)
    documents_label = documents_label_template % version
    return get_property_value(path_dataset,documents_label)

def set_cluster_mode():
    global cluster_mode
    cluster_mode=True

def set_windows_mode():
    global windows_mode
    windows_mode=True

def get_root():
    if cluster_mode:
        return "hdfs://nn.hdfs.webis.de:8020/user/befi8957/topic-ontologies"
    elif windows_mode:
        return "C:\\Users\\user\\disk1\\"
    else:
        return "/mnt/ceph/storage/data-in-progress/data-research/arguana/topic-ontologies"