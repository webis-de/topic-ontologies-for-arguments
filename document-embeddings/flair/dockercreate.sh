#!/bin/bash
GPU=$1

nvidia-docker run \
  --name=dogu3912-$GPU \
  --user=$(id -u):$(id -g) \
  --env=NVIDIA_VISIBLE_DEVICES=$GPU \
  --env=NVIDIA_DRIVER_CAPABILITIES=compute,utility \
  --env=LD_LIBRARY_PATH=/usr/local/nvidia/lib:/usr/local/nvidia/lib64 \
  --volume=/home/dogu3912/dogu3912/topic-ontologies-for-argumentation/document-embeddings/flair:/workspace \
  --workdir=/workspace \
  --restart=no \
  --detach=true \
  pytorch/pytorch:1.3-cuda10.1-cudnn7-runtime \
  tail -f /dev/null
