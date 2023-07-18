#!/bin/bash
for i in $(seq 0 23);do
  for weighted in true;do
    for embedding in elmo;do
      ./task $i $weighted $embedding
    done
  done
done
