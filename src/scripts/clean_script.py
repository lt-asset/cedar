import os
import argparse
import sys

def read_file(path):
    with open(path) as file:
        ret = file.readlines()
    return ret

def get_buggy_file_docter(sub_dir, bug_type):
    # sub_dir: .../pytorch-09-21-2022-23-00-01/conform_constr/torch.abs.yaml_workdir
    all_buggy_py = []
    all_buggy_seed = []
    for bt in bug_type:
        record_path = os.path.join(sub_dir, bt+'_record')
        script_record_path = os.path.join(sub_dir, bt+'_script_record')
        if os.path.exists(record_path):
            all_buggy_py += [x.replace('\n', '').replace('python ', '') for x in read_file(script_record_path)]
            all_buggy_seed += [x.replace('\n', '') for x in read_file(record_path)]
    # all_buggy_py = [x.replace('python ', '') for x in all_buggy_py]
    return all_buggy_py, all_buggy_seed

def get_all_file(sub_dir):
    # sub_dir: .../pytorch-09-21-2022-23-00-01/conform_constr/torch.abs.yaml_workdir
    all_py = []
    all_seed = []

    for f in os.listdir(sub_dir):
        if f.endswith('.p'):
            all_seed.append(os.path.join(sub_dir,f)) 
        if f.endswith('.py'):
            all_py.append(os.path.join(sub_dir,f))

    return all_py, all_seed

def get_eagle_buggy_seed(list_path):
    return [x.replace('\n', '') for x in read_file(list_path)]


def main(exp_folder):
    bug_type = ['Floating_Point_Exception', 'Segmentation_Fault', 'Abort', 'Bus_Error', 'Kill', 'Nan', 'Division_By_Zero']
    mode = ['conform_constr', 'violate_constr']

    # the seed EAGLE need to save
    eagle_buggy_seed = get_eagle_buggy_seed(os.path.join(exp_folder, 'doctor_save_list.txt'))
    py_removed = 0
    seed_removed = 0
    space_released = 0
    for m in mode:
        # workdir: pytorch/pytorch-09-21-2022-23-00-01/conform_constr
        workdir = os.path.join(exp_folder, m)
        sub_dir = [f.path for f in os.scandir(workdir) if f.is_dir()]  # all the API folders
        for d in sub_dir:
            # d: pytorch/pytorch-09-21-2022-23-00-01/conform_constr/torch.cuda.memory_summary.yaml_workdir
            all_py, all_seed = get_all_file(d)
            docter_buggy_py, docter_buggy_seed = get_buggy_file_docter(d, bug_type)
            for seed in all_seed:
                if seed not in docter_buggy_seed and seed not in eagle_buggy_seed:
                    seed_removed += 1
                    space_released += os.path.getsize(seed)
                    print('Remove seed: ' + str(seed))
                    os.remove(seed)
                else:
                    print('Keep seed: ' + str(seed))
            
            for py in all_py:
                if py not in docter_buggy_py:
                    py_removed += 1
                    space_released += os.path.getsize(py)
                    print('Remove python: ' + str(py))
                    os.remove(py)
                else:
                    print('Keep python: ' + str(py))

    print('Removed {} seeds and {} python scripts in total'.format(seed_removed, py_removed))
    print('Released {} bytes in total'.format(space_released))
if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('exp_folder')
    args = parser.parse_args()
    main(args.exp_folder)
