#!/bin/bash

function run_on_test() {
  ontology=$1
  is_tuned=$2

  model=pretrained
  tuned=""
  if [ $is_tuned -eq 1 ];then
    model=$ontology
    if [ $(echo "$ontology" | grep "strategic-intelligence" | wc -l) -eq 1 ];then
      model=$ontology-sample
    fi
    tuned="-tuned"
  fi

  echo "Suggestions for $ontology is_tuned=$is_tuned"
  python3 src/python/suggest.py data/test-arguments-ids.txt data/test-arguments-embedded-for-$model.txt data/$ontology-topic-ids.txt data/$ontology$tuned.txt "bert$tuned" > output/test-arguments-$ontology-bert$tuned.csv
  echo "Validation for $ontology is_tuned=$is_tuned"
  python3 src/python/get-valid-suggestions.py output/test-arguments-$ontology-bert$tuned.csv valid-topic-ids.txt output/test-arguments-$ontology-bert$tuned-valid.csv
}

for ontology in debatepedia wikipedia-categories wikipedia strategic-intelligence strategic-intelligence-sub-topics;do
  run_on_test $ontology 0
done

k=10
echo "Top $k for is_tuned=0"
python3 src/python/get-topk-suggestions.py output/test-arguments-{debatepedia,wikipedia,wikipedia-categories,strategic-intelligence,strategic-intelligence-sub-topics}-bert-valid.csv $k output/test-arguments-top"$k"suggestions-bert.csv

echo "All done"

