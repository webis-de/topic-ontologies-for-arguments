#!/bin/bash
mkdir -p data
mkdir -p output
cp /mnt/ceph/storage/data-in-progress/args-topic-modeling/resources/corpora/*-topic-ids.txt data/
cp /mnt/ceph/storage/data-in-progress/args-topic-modeling/resources/bert/concepts/* data/
cp /mnt/ceph/storage/data-in-progress/args-topic-modeling/resources/bert/arguments/test-arguments-* data/
