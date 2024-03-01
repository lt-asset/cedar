#!/bin/bash

package=$1
workdir=$2

if [[ "$package" != "tensorflow" && "$package" != "pytorch" && "$package" != "mxnet" ]];then
  echo "Error: unsupported package choice: $package"
  exit 1
fi


echo "===== Start DocTer ====="
bash run_DocTer.sh $package $workdir > $workdir/docter.log
echo "===== Start EAGLE ====="
bash run_EAGLE.sh $package $workdir > $workdir/eagle.log
echo "===== Clearning scripts ====="
python /home/code/nightly-docter-eagle/scripts/clean_script.py $workdir > $workdir/clean.log