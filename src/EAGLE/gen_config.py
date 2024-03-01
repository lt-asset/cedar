import sys

def gen_config(lib, workdir_path):
    config_path = "EAGLE/config.py"

    with open(config_path, "r") as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if "DATA_DIR" in line:
            lines[i] = "DATA_DIR = \"" + str(workdir_path) + "\"\n"
        elif "NUM_OF_ARGS" in line:
            if lib == "tensorflow":
                lines[i] = "NUM_OF_ARGS = 50\n"
            elif lib == "pytorch":
                lines[i] = "NUM_OF_ARGS = 200\n"
        elif "NUM_OF_INPUT" in line:
            if lib == "tensorflow":
                lines[i] = "NUM_OF_INPUT = 50\n"
            elif lib == "pytorch":
                lines[i] = "NUM_OF_INPUT = 200\n"

    with open(config_path, "w") as f:
        f.writelines(lines)

if __name__ == "__main__":
    gen_config(sys.argv[1], sys.argv[2])