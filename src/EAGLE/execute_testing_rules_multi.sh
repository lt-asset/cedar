#!/bin/bash

# set cwd to the directory of this script
cd "${0%/*}"

LIB=${1}
VER=${2}
workdir_path=${3}

log_dir="$workdir_path/logs"

if [ ! -d $log_dir ] 
then
    echo "create dir $log_dir"
    mkdir $log_dir
fi

now="$(date +"%y_%m_%d_%H_%M_%S")"
LOG_FILE="$log_dir/testing_${LIB}_${VER}_$now.log"

exec &>$LOG_FILE

python execute_testing_rules_multi.py $LIB $VER