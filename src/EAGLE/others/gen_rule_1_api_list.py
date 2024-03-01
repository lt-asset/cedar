import os


def gen_api_list_tf(in_dir):
    dir_list = os.listdir(in_dir)
    content = ""
    for dir in dir_list:
        content += dir
        content += "\n"
    api_list_file = "rule_1_tensorflow_api_list.txt"
    with open(api_list_file, "w") as f:
        f.write(content)

if __name__ == "__main__":
    in_dir = "/mnt/equivalentmodels_data/generated_input/args/tensorflow/21"
    gen_api_list_tf(in_dir)

