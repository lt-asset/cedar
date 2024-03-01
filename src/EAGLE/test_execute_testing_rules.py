import os
import subprocess
import argparse

from timeit import default_timer as timer

import running_utils
from config import DATA_DIR, NUM_OF_INPUT, TEST_DONE_COLS, TEST_DONE_FILE


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("lib", choices=['tensorflow', 'pytorch'])
    parser.add_argument("version", type=str)
    args = parser.parse_args()
    config = vars(args)

    lib = config['lib']
    version = config['version']

    in_dir = os.path.join(DATA_DIR, "generated_input")
    # in_dir = os.path.join(DATA_DIR, "generated_input_bak")
    out_dir = os.path.join(DATA_DIR, "test_rule_output")

    done_set, done_out_f = running_utils.setup_done_file(out_dir, TEST_DONE_FILE, TEST_DONE_COLS)
    done_out_f.close()

    rule_list = [
        "rule_1",
        "rule_2",  # pass
        "rule_3",  # pass
        "rule_4",
        # "rule_5",
        "rule_6",
        "rule_7",  # passg
        "rule_8",
        "rule_9",  # pass
        "rule_10",
        "rule_11",  # pass
        "rule_12",  # pass
        "rule_13",
        "rule_14",
        "rule_15",
        "rule_16",
    ]

    #comment to run all input
    # NUM_OF_INPUT = 10

    for rule in rule_list:
        if rule == "rule_15" or rule == "rule_16":
            NUM_OF_INPUT = 1
        else:
            NUM_OF_INPUT = 10
        api_list_file = os.path.join("rules", "%s_%s_api_list.txt" % (rule, lib))
        api_list = running_utils.load_list(api_list_file)

        count = 0

        for api in api_list:
            rule_script = "%s_%s_script" % (rule, lib)
            for input_index in range(NUM_OF_INPUT):
                if (rule, lib, version, api, str(input_index), 'done') not in done_set and (rule, lib, version, api,
                                                                                            str(input_index),
                                                                                            'error') not in done_set:
                    command = "python -m rules.%s '%s' '%s' %s %s %s %d" % (rule_script, in_dir, out_dir, lib, version,
                                                                            api, input_index)
                    print("Executing: %s" % command)

                    start_time = timer()
                    status = subprocess.call(command, shell=True)
                    end_time = timer()
                    test_time = end_time - start_time

                    if status == 0:
                        success = 'done'
                    else:
                        success = 'error'

                    conf = {
                        'rule': rule,
                        'lib': lib,
                        'version': version,
                        'api': api,
                        'input_index': str(input_index),
                        'done': success
                    }

                    running_utils.write_done(conf, test_time, out_dir, TEST_DONE_FILE, cols=TEST_DONE_COLS)

            count += 1
            if count >= 1:   # test first x api for each rule
                break


if __name__ == "__main__":
    main()
