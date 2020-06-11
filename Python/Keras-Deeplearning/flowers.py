"""
Image detection with flowers in keras

Disable the terrible logs

WIP
"""
import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Dropout, MaxPooling2D

import tensorflow as tf
import numpy as np
import pathlib
from time import sleep

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
BATCH_SIZE = 1
IMG_HEIGHT = 20
IMG_WIDTH = 20
EPOCHS = 5
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

################### TRAINING

model_new = Sequential([
    Conv2D(16, 3, padding='same', activation='relu', 
           input_shape=(IMG_HEIGHT, IMG_WIDTH ,3)),
    MaxPooling2D(),
    Dropout(0.2),
    Conv2D(32, 3, padding='same', activation='relu'),
    MaxPooling2D(),
    Conv2D(64, 3, padding='same', activation='relu'),
    MaxPooling2D(),
    Dropout(0.2),
    Flatten(),
    Dense(255, activation='relu'),
    Dense(1)
])

model_new.compile(optimizer='adam',
                  loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
                  metrics=['accuracy'])

model_new.summary()

history = model_new.fit(
    train_data_gen,
    steps_per_epoch=STEPS_PER_EPOCH,
    epochs=EPOCHS,

)
