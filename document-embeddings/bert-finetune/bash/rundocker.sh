gpu=$1
docker run --detach --init \
  --name=dogu3912-$gpu \
  --runtime=nvidia \
  --ipc=host \
  --user="$(id -u):$(id -g)" \
  --volume="$PWD:/app" \
  -e NVIDIA_VISIBLE_DEVICES=$gpu \
  anibali/pytorch tail -f /dev/null
