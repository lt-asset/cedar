#!/bin/bash


home='/home' 
repo_name="nightly-docter-eagle"   

package=$1
constraints_folder=$2
config_path=$3
workdir_path=$4
MAX_PROC=${5:-2}   # optional argument, default 2
TIMEOUT=7200  #2h

FUZZERGIT="$home"/code/"$repo_name"

. $config_path

if [[ "$package" != "tensorflow" && "$package" != "pytorch" && "$package" != "mxnet" && "$package" != "sklearn" ]];then
  echo "Error: unsupported package choice: $package"
  exit 1
fi

if [[ "$mode" != "conform" && "$mode" != "violate" ]];then
  echo "Error: unsupported mode choice: $mode. Supported mode: conform or violate"
  exit 1
fi

if [[ "$constr" != "yes" && "$constr" != "no" ]];then
  echo "Error: unsupported constr choice: $constr. Supported constr: yes or no"
  exit 1
fi

subdir="$mode"

if [ "$constr" == "yes" ]; then
    subdir+="_constr"
else
    subdir+="_noconstr"
fi

WORKDIR=$workdir_path/"$subdir"
workorder_record="$WORKDIR"/"record_work"
if [ -f "$workorder_record" ]; then
  echo "... record_work exists ..."
else
  mkdir -p "$WORKDIR"
  touch "$workorder_record"
fi

fail_log_path="$WORKDIR"/"$mode"_fail.log
touch $fail_log_path

function call_fuzzer(){
  # files=("$constraints_folder"/*)
  fname=$1
  name=$( basename "$fname" )
  if grep -qw "$name" "$workorder_record"; then
    echo "Skipping $name"
    return 1
  fi
  # else
  #   echo "$name" >> $workorder_record
  # fi

  API_workdir="$WORKDIR/${name}_workdir"
  mkdir -p "$API_workdir"
  args=(
    "$fname"
    "${FUZZERGIT}/${package}/${package}_dtypes.yml"
    "--workdir=$API_workdir"
    "--fuzz_optional_p=$fuzz_optional_p"
    "--guided_mutate"
    "--mutate_p=$mutate_p"
    "--timeout=$timeout"
    "--max_iter=$max_iter"
    "--save_cnt=$save_cnt"
    "--model_test"
    "--check_nan"
    "--gen_script"
  )
  if [ "$constr" == "no" ]; then # baseline
    args+=("--ignore")
  fi

  if [ "$mode" == "conform" ]; then
    args+=("--conform")
  fi

  if [ "$package" == "pytorch" ];then
    args+=("--data_construct=tensor")
  elif [ "$package" == "mxnet" ];then
    args+=("--data_construct=nd.array")
  fi

  if [ "$save_script" == "yes" ]; then 
    args+=("--save")
  fi




  # echo "python ${FUZZERGIT}/fuzzer/fuzzer-driver.py "${args[@]}" &> $workdir/out"
  echo "===  [$mode] $( basename "$fname" ) ===    started"
  fuzzer_args="${args[@]}"
  touch "$API_workdir/eagle_order"
  timeout $TIMEOUT bash -c "python ${FUZZERGIT}/fuzzer/fuzzer-driver.py $fuzzer_args &> $API_workdir/out"
  status=$?
  if [ $status -eq 0 ];then
    status_msg="done"
    echo "$name" >> $workorder_record
  else
    echo $fname >> $fail_log_path
    status_msg="fail"
  fi
  echo "===  [$mode] $( basename "$fname" ) ===    $status_msg"
}

echo "Start fuzzing in mode $mode, Maximum process: $MAX_PROC"

files=("$constraints_folder"/*)
jobs_to_run_num=${#files[@]}
jobs_cntr=0
check_interval=10


while ((jobs_cntr < jobs_to_run_num)); do 
    cur_jobs_num=$(wc -l < <(jobs -r))

    if ((cur_jobs_num <= MAX_PROC)); then 
        # echo -e "cur_jobs_num\t${cur_jobs_num}"
        call_fuzzer ${files[jobs_cntr]} &
        ((jobs_cntr++))
        echo "=== [$mode] Progress: $jobs_cntr/$jobs_to_run_num ==="
    # sleep is needed to reduce the frequency of while loop
    # otherwise it itself will eat a lot of processor time
    # by restlessly checking
    else
        sleep "$check_interval"
    fi  
done

wait    # wait all process finish
echo "===  [$mode] Finished fuzzing all APIs ==="


echo "===  [$mode] Rerun failed APIs ==="

while read -r line; do
    name=$( basename "$line" )
    mv "$WORKDIR"/"$name"_workdir "$WORKDIR"/failed_"$name"_workdir
    call_fuzzer $line &
done < $fail_log_path


wait    # wait all process finish
echo "===  [$mode] Finished reruning failed APIs ==="
