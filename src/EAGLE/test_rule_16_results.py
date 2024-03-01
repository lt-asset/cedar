import pickle

path1 = ""

with open(path1, "rb") as f:
    outputs = pickle.load(f)

[[output_1, metrics_value_1, config_1, weight_1], [output_2, metrics_value_2, config_2, weight_2]] = outputs

print(config_1 == config_2)
