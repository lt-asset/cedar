#!/bin/bash

package=$1
workdir_path=$2

version_dir=$(basename $workdir_path)

if [[ "$package" != "tensorflow" && "$package" != "pytorch" ]];then
  echo "Error: unsupported package choice: $package"
  exit 1
fi

echo "===== Start EAGLE ====="
date '+%T.%N'

if [[ "$package" == "tensorflow" ]];then
  echo "===== Installing TensorFlow IO ====="
  pip install tensorflow-io[tensorflow]
  pip install --upgrade keras
fi



python EAGLE/gen_config.py $package $workdir_path


echo "===== Generate customized input  ====="
date '+%T.%N'
bash EAGLE/generate_all_input.sh $package $version_dir $workdir_path
if [[ "$package" == "tensorflow" ]];then
  python EAGLE/others/gen_rule_16_tf_config.py $workdir_path
else
  python EAGLE/others/gen_rule_16_pt_config.py $workdir_path
fi

echo "===== Run eagle on rule 1 - 14 ====="
date '+%T.%N'
bash EAGLE/execute_testing_rules_multi.sh $package $version_dir $workdir_path

echo "===== Run eagle on rule 15 - 16 ====="
date '+%T.%N'
bash EAGLE/execute_testing_rules_15_16_multi.sh $package $version_dir $workdir_path

echo "===== Result analysis ====="
date '+%T.%N'
cd EAGLE
python analyze_results.py $package $version_dir

echo "===== Cleaning ====="
python cleaning_input.py $package $version_dir

echo "===== Removing rule_output ====="
du -sh $workdir_path/rule_output
rm -r $workdir_path/rule_output

echo "===== EAGLE finished ====="
date '+%T.%N'
