import functools

import numpy as np
import pandas as pd
import tensorflow as tf

import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

# URL with titanic dataset
TRAIN_DATA_URL = "https://storage.googleapis.com/tf-datasets/titanic/train.csv"
TEST_DATA_URL = "https://storage.googleapis.com/tf-datasets/titanic/eval.csv"

# Download train data and test data
train_file_path = tf.keras.utils.get_file("train.csv", TRAIN_DATA_URL)
test_file_path = tf.keras.utils.get_file("eval.csv", TEST_DATA_URL)

# Round values to 3 digits
np.set_printoptions(precision=3, suppress=True)

# Mark the labels
LABEL_COLUMN = "survived"
LABELS = [0, 1]


def get_dataset(file_path, **kwargs):
    # Create a dataset
    dataset = tf.data.experimental.make_csv_dataset(
        file_path,
        batch_size=5,
        label_name=LABEL_COLUMN,
        na_value="?",
        num_epochs=1,
        ignore_errors=True,
        **kwargs
    )
    return dataset


# Create raw train data and test data
raw_train_data = get_dataset(train_file_path)
raw_test_data = get_dataset(test_file_path)


def show_batch(dataset):
    """Show the batch in the terminal"""
    for batch, label in dataset.take(1):
        for key, value in batch.items():
            print("{:20s}: {}".format(key, value.numpy()))


SELECT_COLUMNS = ["survived", "age", "n_siblings_spouses", "parch", "fare"]
DEFAULTS = [0, 0.0, 0.0, 0.0, 0.0]
temp_dataset = get_dataset(
    train_file_path, select_columns=SELECT_COLUMNS, column_defaults=DEFAULTS
)

example_batch, labels_batch = next(iter(temp_dataset))


def pack(features, label):
    return tf.stack(list(features.values()), axis=-1), label


packed_dataset = temp_dataset.map(pack)

for features, labels in packed_dataset.take(1):
    print(features.numpy())
    print()
    print(labels.numpy())

desc = pd.read_csv(train_file_path)[NUMERIC_FEATURES].describe()
MEAN = np.array(desc.T["mean"])
STD = np.array(desc.T["std"])

print(std)
print(mean)
