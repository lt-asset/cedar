rule_file_list = ["rule_15_tensorflow_api_list.txt", "rule_16_tensorflow_api_list.txt"]

for rule_file in rule_file_list:
    with open(rule_file, "r") as f:
        lines = f.readlines()
        content = ""
        for line in lines:
            new_line = line.replace(" ", "")
            content += new_line
            if not new_line.endswith("\n"):
                content += "\n"

    with open(rule_file, "w") as f:
        f.write(content)
