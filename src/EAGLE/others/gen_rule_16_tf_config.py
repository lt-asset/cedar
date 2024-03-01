import pickle
import os
import random
import sys

import tensorflow as tf
import numpy as np

model_list = [
    tf.keras.applications.DenseNet121,
    tf.keras.applications.DenseNet169,
    tf.keras.applications.DenseNet201,
    tf.keras.applications.InceptionResNetV2,
    tf.keras.applications.InceptionV3,
    tf.keras.applications.MobileNet,
    tf.keras.applications.MobileNetV2,
    tf.keras.applications.NASNetLarge,
    tf.keras.applications.NASNetMobile,
    tf.keras.applications.ResNet101,
    tf.keras.applications.ResNet101V2,
    tf.keras.applications.ResNet152,
    tf.keras.applications.ResNet152V2,
    tf.keras.applications.ResNet50,
    tf.keras.applications.ResNet50V2,
    tf.keras.applications.VGG16,
    tf.keras.applications.VGG19,
    tf.keras.applications.Xception
]

def save_model_and_inputs(model_save_dir):
    if not os.path.exists(model_save_dir):
        os.makedirs(model_save_dir)
    for index in range(len(model_list)):
        model = model_list[index]()
        input_shape = model.input_shape
        print(input_shape)
        if len(input_shape) == 3:
            dim0, dim1, dim2 = input_shape
        elif len(input_shape) == 4:
            _, dim0, dim1, dim2 = input_shape
        else:
            print(input_shape)
            raise Exception("Unkown input shape")

        x_list = np.random.randn(10, dim0, dim1, dim2)
        y_list = np.random.randint(0, 1000, size=10)
        input_file = [x_list, y_list]

        model_save_path = os.path.join(model_save_dir, "model_{}".format(index))
        tf.keras.models.save_model(model, model_save_path)

        input_save_path = os.path.join(model_save_dir, "input_{}".format(index))
        with open(input_save_path, "wb") as f:
            pickle.dump(input_file, f)



model_file_list = [
    "model_0",
    "model_1",
    "model_2",
    "model_3",
    "model_4",
    "model_5",
    "model_6",
    "model_7",
    "model_8",
    "model_9",
    "model_10",
    "model_11",
    "model_12",
    "model_13",
    "model_14",
    "model_15",
    "model_16",
    "model_17",
]

input_file_list = [
    "input_0",
    "input_1",
    "input_2",
    "input_3",
    "input_4",
    "input_5",
    "input_6",
    "input_7",
    "input_8",
    "input_9",
    "input_10",
    "input_11",
    "input_12",
    "input_13",
    "input_14",
    "input_15",
    "input_16",
    "input_17",
]

optimizer_list = [
    "adadelta",
    "adagrad",
    "adam",
    "adamax",
    "ftrl",
    "nadam",
    "rmsprop",
    "sgd",
]

loss_list = [
    "categorical_crossentropy",
    "cosine_similarity",
    "categorical_hinge",
    "sparse_categorical_crossentropy",
    "logcosh",
    "poisson",
    "mse",
]

metrics_list = [
    "Accuracy",
]

save_load_mode = [
    "model",
    "config",
    "weights",
]

def random_generate_config_16():
    with open("/mnt/tmp/tf2.1_rule_18", "w") as f:
        for i in range(400):
            index = random.randint(0, 17)
            model_file = os.path.join(model_save_dir, model_file_list[index])
            input_file = os.path.join(model_save_dir, input_file_list[index])
            optimizer = random.choice(optimizer_list)
            loss = random.choice(loss_list)
            metrics = random.choice(metrics_list)
            save_load_mode_list = random.choice(save_load_mode)
            line = model_file + '-' \
                    + input_file + '-' \
                    + optimizer + '-' \
                    + loss + '-' \
                    + metrics + '-' \
                    + save_load_mode_list + "\n"
            f.write(line)


if __name__ == "__main__":
    in_dir = sys.argv[1]
    model_save_dir = os.path.join(in_dir, "generated_input/saved_model")
    save_model_and_inputs(model_save_dir)
    # random_generate_config_16()
