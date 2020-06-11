"""
Image detection with flowers in keras

Disable the terrible logs

WIP
"""
import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

from tensorflow.keras.layers import Flatten, Dense, Dropout
import tensorflow as tf
import numpy as np
import pathlib

"""
Download a flower dataset and extract it
"""
data_dir = tf.keras.utils.get_file(
    origin="https://storage.googleapis.com/download.tensorflow.org/example_images/flower_photos.tgz",
    fname="flower_photos",
    untar=True,
)
data_dir = pathlib.Path(data_dir)

# Use Autotune
AUTOTUNE = tf.data.experimental.AUTOTUNE

# Get all classes and the image count
CLASS_NAMES = np.array(
    [item.name for item in data_dir.glob("*") if item.name != "LICENSE.txt"]
)
image_count = len(list(data_dir.glob("*/*.jpg")))

# Settings
BATCH_SIZE = 32
IMG_HEIGHT = 224
IMG_WIDTH = 224
STEPS_PER_EPOCH = np.ceil(image_count / BATCH_SIZE)

# Rescale images from 8 bit to 1 bit
image_generator = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1.0 / 255)

# Prepare
train_data_gen = image_generator.flow_from_directory(
    directory=str(data_dir),
    batch_size=BATCH_SIZE,
    shuffle=True,
    target_size=(IMG_HEIGHT, IMG_WIDTH),
    classes=list(CLASS_NAMES),
)

# List all files inside of the datadir
list_ds = tf.data.Dataset.list_files(str(data_dir / "*/*"))


def get_label(file_path):
    # convert the path to a list of path components
    parts = tf.strings.split(file_path, os.path.sep)
    # The second to last is the class-directory
    return parts[-2] == CLASS_NAMES


def decode_img(img):
    # convert the compressed string to a 3D uint8 tensor
    img = tf.image.decode_jpeg(img, channels=3)
    # Use `convert_image_dtype` to convert to floats in the [0,1] range.
    img = tf.image.convert_image_dtype(img, tf.float32)
    # resize the image to the desired size.
    return tf.image.resize(img, [IMG_HEIGHT, IMG_WIDTH])


def process_path(file_path):
    label = get_label(file_path)
    # load the raw data from the file as a string
    img = tf.io.read_file(file_path)
    img = decode_img(img)
    return img, label


def prepare_for_training(ds, cache=True, shuffle_buffer_size=1000):
    # This is a small dataset, only load it once, and keep it in memory.
    # use `.cache(filename)` to cache preprocessing work for datasets that don't
    # fit in memory.
    if cache:
        if isinstance(cache, str):
            ds = ds.cache(cache)
        else:
            ds = ds.cache()

    ds = ds.shuffle(buffer_size=shuffle_buffer_size)

    # Repeat forever
    ds = ds.repeat()

    ds = ds.batch(BATCH_SIZE)

    # `prefetch` lets the dataset fetch batches in the background while the model
    # is training.
    ds = ds.prefetch(buffer_size=AUTOTUNE)

    return ds


def show_batch(image_batch, label_batch):
    from PIL import Image
    import numpy as np
    import matplotlib.pyplot as plt

    plt.figure(figsize=(10, 10))
    for n in range(25):
        ax = plt.subplot(5, 5, n + 1)
        plt.imshow(image_batch[n])
        plt.title(CLASS_NAMES[label_batch[n] == 1][0].title())
        plt.axis("off")
    plt.show()


# Set `num_parallel_calls` so multiple images are loaded/processed in parallel.
labeled_ds = list_ds.map(process_path, num_parallel_calls=AUTOTUNE)
train_ds = prepare_for_training(labeled_ds)
################### TRAINING


model = tf.keras.models.Sequential(
    [
        Flatten(input_shape=(244, 244)),
        Dense(64, activation="relu"),
        Dropout(0.2),
        Dense(10),
    ]
)

"""
Computes the crossentropy loss between the labels and predictions.
"""
loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)

""" 
Set the model to minimize loss.
Use the Adam optimizer.
"""
model.compile(optimizer="adam", loss=loss_fn, metrics=["accuracy"])

"""
Train with X and Y data
Give the model 5 epochs
"""
model.fit(train_ds, labeled_ds, epochs=5)

"""
Test our model with our test data
"""
