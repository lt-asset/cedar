import numpy as np

def convert_rule_16_tf():
    with open("rule_16_tensorflow_api_list.txt", "r") as f:
        lines = f.readlines()

    new_content = ""
    for line in lines:
        preprocess_line = line.split("-")
        model_name = preprocess_line[0]
        input_file = preprocess_line[1]
        optimizer = preprocess_line[2]
        loss_fun = preprocess_line[3]
        metrics = preprocess_line[4]
        save_load_mode = preprocess_line[5]

        input_file = input_file.split("/")
        input_file = input_file[-1]
        model_name = model_name.split("/")
        model_name = model_name[-1]

        new_content += model_name + "-" + input_file + "-" + optimizer + "-" + loss_fun + "-" + metrics + "-" + save_load_mode

    with open("rule_16_tensorflow_api_list.txt", "w") as f:
        f.write(new_content)


def convert_rule_15_tf():
    with open("rule_15_tensorflow_api_list.txt", "r") as f:
        lines = f.readlines()

    new_content = ""
    for line in lines:
        preprocess_line = line.split("-")
        model_name = preprocess_line[0]
        input_file = preprocess_line[1]
        optimizer = preprocess_line[2]
        loss_fun = preprocess_line[3]
        metrics = preprocess_line[4]
        save_load_mode = preprocess_line[5]

        s1 = 0
        s2 = 0
        while(s1 == s2):
            s1 = np.random.randint(1, 100)
            s2 = np.random.randint(1, 100)

        batch_size_1 = str(s1)
        batch_size_2 = str(s2)

        new_content += model_name + "-" + input_file + "-" + optimizer + "-" + loss_fun + "-" + metrics + "-" + batch_size_1 + "-" + batch_size_2 + "\n"

    with open("rule_15_tensorflow_api_list.txt", "w") as f:
        f.write(new_content)

def convert_rule_16_pt():
    with open("rule_16_pytorch_api_list.txt", "r") as f:
        lines = f.readlines()

    new_content = ""
    for line in lines:
        preprocess_line = line.split("-")
        model_path = preprocess_line[0]
        input_file = preprocess_line[1]
        save_load_mode = preprocess_line[2]

        input_file = input_file.split("/")
        input_file = input_file[-1]

        new_content += model_path + "-" + input_file + "-" + save_load_mode

    with open("rule_16_pytorch_api_list.txt", "w") as f:
        f.write(new_content)

def convert_rule_15_pt():
    with open("rule_15_pytorch_api_list.txt", "r") as f:
        lines = f.readlines()

    new_content = ""
    for line in lines:
        preprocess_line = line.split("-")
        model_path = preprocess_line[0]
        input_file = preprocess_line[1]
        save_load_mode = preprocess_line[2]

        input_file = input_file.split("/")
        input_file = input_file[-1]

        s1 = 0
        s2 = 0
        while(s1 == s2):
            s1 = np.random.randint(1, 100)
            s2 = np.random.randint(1, 100)

        batch_size_1 = str(s1)
        batch_size_2 = str(s2)

        new_content += model_path + "-" + input_file + "-" + batch_size_1 + "-" + batch_size_2 + "\n"

    with open("rule_15_pytorch_api_list.txt", "w") as f:
        f.write(new_content)

if __name__ == "__main__":
    # convert_rule_15_tf()
    # convert_rule_16_tf()

    convert_rule_15_pt()
    # convert_rule_16_pt()
