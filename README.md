## Topic Ontologies for Arguments

This repository contains the code and evaluation scripts for matching the data of 59 argument corpora with three topic 
ontologies. The data used in this experiment can be found  [here](https://zenodo.org/record/5180409).

### Preprocessing 59 argument corpora 
The units and topics sof 59 argument corpora were cleaned and organized with an individual script for each corpus in 
[preprocessing](preprocessing)
### Preparing for Manual matching 

Manually matching the topics of 39 argument corpora with the topics of three topic ontologies was done manually using the judgment interface. 
Candidate topic matches were generated using BM25 (Whoosh) in 
[manual topic_matching](manual_topic_matching)

### Matching the a sample of 104 with the topics of three topic ontologies
Automatically matching units with topic ontologies were implemented using two approaches semantic indexing (explicit semantic analysis)
and bert (and other transformers). These approaches were evaluated in a depth of 5 pooling setup which was carried out using the 
judgement interface. The implementation for the two aproaches can be found here and a baseline can be found here.

[direct-match-baseline](direct-match-baseline)

[explicit semantic analysis](esa)

[bert and other transformers](document-embeddings)

### Evaluation 

To evaluate the suggestions of the three approaches the following script can be used.

[automatic topic matching evaluation](automatic_topic_matching_evaluation)

### Judgement Interface
The judgement interface was used for both manual matching of units with the three topic ontologies and the evaluation 
of the automatic appraoches.

[judgement interface](judgement-interface)


## Citation

Topic Ontologies for Arguments has been published in Findings of EACL 2023 ["Topic Ontologies for Arguments"](https://aclanthology.org/2023.findings-eacl.104/)
which can be cited as follows:

```
@InProceedings{ajjour:2023,
  author =                   {Yamen Ajjour and Johannes Kiesel and Benno Stein and Martin Potthast},
  booktitle =                {17th Conference of the European Chapter of the Association for Computational Linguistics (EACL 2023)},
  month =                    may,
  numpages =                 17,
  publisher =                {Association for Computational Linguistics},
  site =                     {Dubrovnik, Croatia},
  title =                    {{Topic Ontologies for Arguments}},
  todo =                     {dataurl, doi, editor, url, pages},
  year =                     2023
}
```
