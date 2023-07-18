#!/bin/bash
input=$1
max_per_class=$2

head -n 1 $input
tail -n +2 $input \
  | shuf \
  | awk -F, '{
      label = $NF
      cnt[label] += 1
      if (cnt[label] <= '$max_per_class') {
        print $0
      }
    }'
