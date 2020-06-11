"""
Fully writen out version of:
https://www.tensorflow.org/tutorials/quickstart/beginner
"""
# Disable the terrible logs
import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"


import tensorflow as tf

from tensorflow.keras.layers import Flatten, Dense, Dropout

"""
Dataset of handwritten digits
http://yann.lecun.com/exdb/mnist/
"""
mnist = tf.keras.datasets.mnist

"""
x is the sample.
y is the label.
Ror example x the given values and y is the answer
"""
(x_train, y_train), (x_test, y_test) = mnist.load_data()

"""
x_train and x_test are currently 8 bit pixels
We need to convert the 8bit pixels to a float by dividing it by 255
"""
x_train, x_test = x_train / 255.0, x_test / 255.0

"""
The samples are each 28x28 pixels
ReLU = rectified linear
https://en.wikipedia.org/wiki/Rectifier_(neural_networks)
This given model has 10 output nodes
"""
model = tf.keras.models.Sequential(
    [
        Flatten(input_shape=(28, 28)),
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
model.fit(x_train, y_train, epochs=5)

"""
Test our model with our test data
"""
model.evaluate(x_test, y_test, verbose=2)
