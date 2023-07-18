#!/bin/bash
for i in $(seq 0 23);do
  for weighted in false;do
    #for embedding in flair glove elmo bert;do
    for embedding in bert;do
      #for ontology in debatepedia wikipedia-level{1,2} world-economic-forum-level{1,2};do
      for ontology in wikipedia-level1;do
        method=$embedding
        if [ "$weighted" == "true" ];then
          method=weighted-$method
        fi
        documents=data/doc-embeddings/documents-$i-$method.csv
        topics=data/doc-embeddings/topics-$ontology-$method.csv
        output=data/doc-embeddings/suggestions-$method-$ontology-$i.csv
        if [ -e $output ];then
          echo "Already exists: $output"
        else
          touch $output
          echo "Creating: $output"
          python3 src/python/suggest-for-dense-embeddings.py \
            --documents-file $documents \
            --topics-file $topics \
            --method $method \
            --output-file $output
        fi
      done
    done
  done
done
