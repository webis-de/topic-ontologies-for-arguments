#!/bin/bash
source myvenv/bin/activate

documents_dir=data/documents

for ontology in debatepedia wikipedia-level1 wikipedia-level2 world-economic-forum-level1 world-economic-forum-level2;do
  for documents in $(ls $documents_dir);do
    echo $ontology $documents
    python3 src/python/direct-match.py --documents-file $documents_dir/$documents --topics-file data/topics/$ontology-information.csv --output-file data/direct-match-baseline/suggestions-$documents-$ontology.csv
  done
done
