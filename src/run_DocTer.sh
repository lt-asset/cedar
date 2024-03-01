#!/bin/bash


package=$1
workdir_path=$2

buglist_dest=$workdir_path/bug_list



config_path="./configs/docter.config"
. $config_path




if [ $package == "tensorflow" ]; then
    MAX_PROC=$tf_max_proc
    MAX_PROC_CI=$((MAX_PROC / 2 ))
    MAX_PROC_VI=$((MAX_PROC - MAX_PROC_CI))
     # install nightly version 
    date '+%T.%N'
    echo "=== Install nightly version of TensorFlow ==="
    pip install tf-nightly
    # collect env
    pip list > $workdir_path/pip.log
    echo "==========" >> $workdir_path/pip.log
    python -c "import tensorflow as tf; print(tf.version.GIT_VERSION, tf.version.VERSION)" >> $workdir_path/pip.log
    bash tensorflow/tf_env_collect.sh tmp_out
    mv tmp_out $workdir_path/env.log
    date '+%T.%N'
    # run CI mode
    echo "=== Start DocTer CI mode for TensorFlow ==="
    bash run_fuzzer.sh $package ./all_constr/tf2.1 ./configs/tf_ci.config $workdir_path $MAX_PROC_CI | tee $workdir_path/docter_ci.log &
    # run VI mode
    echo "=== Start DocTer VI mode for TensorFlow ==="
    bash run_fuzzer.sh $package ./all_constr/tf2.1 ./configs/tf_vi.config $workdir_path $MAX_PROC_VI | tee $workdir_path/docter_vi.log &
    # wait for all processes to finish
    wait
    # collect bugs for CI
    echo "=== Finished fuzzing ==="
    date '+%T.%N'
    echo "=== Collecting bug list ==="
    bash scripts/prepare_bug_list.sh $workdir_path/conform_constr/
    # collect bugs for VI
    bash scripts/prepare_bug_list.sh $workdir_path/violate_constr/

    # merge the two bug lists
    cat $workdir_path/conform_constr/bug_list > $buglist_dest
    tail -n +2 $workdir_path/violate_constr/bug_list >> $buglist_dest
    echo "=== Bug list can be found at $buglist_dest ==="
    date '+%T.%N'
elif [ $package == "pytorch" ]; then
    MAX_PROC=$pt_max_proc
    MAX_PROC_CI=$((MAX_PROC / 2 ))
    MAX_PROC_VI=$((MAX_PROC - MAX_PROC_CI))
    # install nightly version 
    date '+%T.%N'
    echo "=== Install nightly version of PyTorch ==="
    pip install --pre torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/nightly/cpu
    # collect env
    pip list > $workdir_path/pip.log
    python pytorch/collect_env.py > $workdir_path/env.log
    
    date '+%T.%N'
    # run CI mode
    echo "=== Start DocTer CI mode for PyTorch ==="
    bash run_fuzzer.sh $package ./all_constr/pt1.5 ./configs/pt_ci.config $workdir_path $MAX_PROC_CI | tee $workdir_path/docter_ci.log &
    # run VI mode
    echo "=== Start DocTer VI mode for PyTorch ==="
    bash run_fuzzer.sh $package ./all_constr/pt1.5 ./configs/pt_vi.config $workdir_path $MAX_PROC_VI | tee $workdir_path/docter_vi.log &
    # wait for all processes to finish
    wait
    # collect bugs for CI
    echo "=== Finished fuzzing ==="
    date '+%T.%N'
    echo "=== Collecting bug list ==="
    bash scripts/prepare_bug_list.sh $workdir_path/conform_constr/
    # collect bugs for VI
    bash scripts/prepare_bug_list.sh $workdir_path/violate_constr/

    # merge the two bug lists
    cat $workdir_path/conform_constr/bug_list > $buglist_dest
    tail -n +2 $workdir_path/violate_constr/bug_list >> $buglist_dest
    echo "=== Bug list can be found at $buglist_dest ==="
    date '+%T.%N'
elif [ $package == "mxnet" ]; then
    MAX_PROC=$mx_max_proc
    MAX_PROC_CI=$((MAX_PROC / 2 ))
    MAX_PROC_VI=$((MAX_PROC - MAX_PROC_CI))
    # https://github.com/dmlc/dgl/issues/1377
    # install nightly version 
    date '+%T.%N'
    echo "=== Install nightly version of MXNet ==="
    # pip install --pre "mxnet-cu102<2" -f https://dist.mxnet.io/python
    pip install --pre "mxnet" -f https://dist.mxnet.io/python
    # collect env
    pip list > $workdir_path/pip.log
    python mxnet/diagnose.py > $workdir_path/env.log
    date '+%T.%N'
    # run CI mode
    echo "=== Start DocTer CI mode for MXNet ==="
    bash run_fuzzer.sh $package ./all_constr/mx1.6 ./configs/pt_ci.config $workdir_path $MAX_PROC_CI | tee $workdir_path/docter_ci.log &
    # run VI mode
    echo "=== Start DocTer VI mode for MXNet ==="
    bash run_fuzzer.sh $package ./all_constr/mx1.6 ./configs/pt_vi.config $workdir_path $MAX_PROC_VI | tee $workdir_path/docter_vi.log &
    # wait for all processes to finish
    wait
    # collect bugs for CI
    echo "=== Finished fuzzing ==="
    date '+%T.%N'
    echo "=== Collecting bug list ==="
    bash scripts/prepare_bug_list.sh $workdir_path/conform_constr/
    # collect bugs for VI
    bash scripts/prepare_bug_list.sh $workdir_path/violate_constr/

    # merge the two bug lists
    cat $workdir_path/conform_constr/bug_list > $buglist_dest
    tail -n +2 $workdir_path/violate_constr/bug_list >> $buglist_dest
    echo "=== Bug list can be found at $buglist_dest ==="
    date '+%T.%N'
else
  echo "Error: unsupported framework choice: $package"
  exit 1

fi