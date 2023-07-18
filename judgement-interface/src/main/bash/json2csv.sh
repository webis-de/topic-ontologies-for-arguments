#!/bin/bash

# Use this file on the judgements.json to convert it to CSV

cat $1 \
  | python -m json.tool \
  | awk 'BEGIN {
      annotators["johannes"] = 1
      annotators["lukas"] = 1
      annotators["yamen"] = 1
    } {
      if ($0~/^            /) {
        topic = $1
        gsub(/^"/, "", topic)
        gsub(/:$/, "", topic)
        gsub(/"$/, "", topic)
        topics[topic] = 1
        judgement = $2
        gsub(/,$/, "", judgement)
        judgements[annotator" "document" "topic] = judgement
        tasks[document" "topic] = 1
      } else if ($0~/^        /) {
        document = $1
        gsub(/^"/, "", document)
        gsub(/:$/, "", document)
        gsub(/"$/, "", document)
      } else if ($0~/^    /) {
        annotator = $1
        gsub(/^"/, "", annotator)
        gsub(/:$/, "", annotator)
        gsub(/"$/, "", annotator)
      }
    } END {
      printf "document.id topic.id"
      countAnnotator = 0
      for (annotator in annotators) {
        countAnnotator += 1
        printf " annotator%d", countAnnotator
      }
      printf ",majority\n"

      n = asorti(tasks, task_names)
      for (i = 1; i <= n; i++) {
        task = task_names[i]
        printf "%s", task
        count_true = 0
        count_annotators = 0
        for (annotator in annotators) {
          printf " %s", judgements[annotator" "task]
          if (judgements[annotator" "task] == "true") {
            countTrue += 1
          }
          countAnnotators += 1
        }
        if (countTrue > countAnnotators / 2) {
          printf ",true"
        } else {
          printf ",false"
        }
        printf "\n"
      }
    }' \
  | sed 's/ /,/g'
