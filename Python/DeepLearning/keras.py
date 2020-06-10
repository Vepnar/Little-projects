"""
Fully writen out version of:
https://www.tensorflow.org/tutorials/quickstart/beginner
"""
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
