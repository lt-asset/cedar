#!/bin/bash

package=$1
workdir=$2

if [[ "$package" != "tensorflow" && "$package" != "pytorch" && "$package" != "mxnet" ]];then
  echo "Error: unsupported package choice: $package"
  exit 1
fi


timestamp=$(date +'%m-%d-%Y-%H-%M-%S')
version_dir=$package"-"$timestamp

echo "===== Create workdir $workdir/$package/$version_dir ====="
mkdir -p $workdir/$package/$version_dir

workdir_path=$workdir/$package/$version_dir
virtual_workdir=/home/workdir/$package/$version_dir

echo "===== Start the container ====="
docker run -v $2:/home/workdir -it -d --name $version_dir dnxie/docter_nightly:latest

echo "===== Start DocTer and EAGLE ====="
docker exec -d -it $version_dir bash -c "bash run.sh $package $virtual_workdir"

echo "===== DocTer and EAGLE running in the background. You are all set! ====="