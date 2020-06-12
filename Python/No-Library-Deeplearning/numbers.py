import os.path
import requests
import numpy as np


DATASET_URL = "https://github.com/SebLague/Mnist-data-numpy-format/raw/master/mnist.npz"
DATASET_FILE = "./mnist.npz"

np.random.seed(1)


def fix_dataset_array(array):
    output = []
    for i in range(len(array)):
        output.append(array[i].flatten())
    return np.array(output)


def load_dataset():
    # Download the dataset when it doesn't exist
    if not os.path.exists(DATASET_FILE):
        print("Downloading dataset...")
        with open(DATASET_FILE, "wb") as file:
            response = requests.get(DATASET_URL)
            file.write(response.content)
        print("Done!")

    with np.load(DATASET_FILE) as dataset:
        return (
            (dataset["training_images"], dataset["training_labels"]),
            (dataset["test_images"], dataset["test_labels"]),
        )


def activation_sigmoid(x, derivative=False):
    """Sigmoid activation function.
    wikipedia: Sigmoid function"""
    if derivative:
        return x * (1 - x)
    return 1 / (1 + np.exp(-x))


def activation_relu(x, derivative=False):
    """Rectified linear unit activation function
    wikipedia: https://en.wikipedia.org/wiki/Rectifier_(neural_networks)
    """
    d = np.maximum(0, x)
    if derivative:
        d[d > 0] = 1
        return d
    return d


class Neural_layer:
    def __init__(self, amount_inputs, amount_neurons, activation_function):
        self.weights = 0.10 * np.random.random((amount_inputs, amount_neurons))
        self.biases = np.zeros((1, amount_neurons))
        self.activation_function = activation_function

    def forward(self, inputs, activation=True):
        dot_product = np.dot(inputs, self.weights) + self.biases
        return self.activation_function(dot_product)

    def reduce_loss(self, layers, labels, predictions, delta, index):
        loss = delta.dot(layers[index + 1].weights.T)
        delta = loss * self.activation_function(predictions[index], derivative=True)
        self.weights += predictions[index - 1].T.dot(delta)
        return delta


class Neural_output(Neural_layer):
    def reduce_loss(self, layers, labels, predictions, delta, index):
        loss = labels - predictions[index + 1]
        delta = loss * self.activation_function(predictions[index + 1], derivative=True)
        self.weights += predictions[index + 1].T.dot(delta)
        self.loss = np.mean(np.abs(loss))
        return delta


class Neural_net:
    def __init__(self, layers):
        self.layers = layers
        self.amount_of_layers = len(self.layers)

    def train(self, inputs, labels):

        # Add our input to our first predictions.
        predictions = [inputs]

        # Calculate predictions.
        for index in range(self.amount_of_layers):
            layer = self.layers[index]
            predictions.append(layer.forward(predictions[-1]))

        delta = None
        for i in range(self.amount_of_layers - 1, 0, -1):
            delta = layers[i].reduce_loss(layers, labels, predictions, delta, i)

        return layers[-1].loss

    def think(self, inputs):
        predictions = [inputs]

        # Calculate predictions.
        for index in range(self.amount_of_layers):
            layer = self.layers[index]
            predictions.append(layer.forward(predictions[-1]))

        return predictions


layers = [
    Neural_layer(4, 64, activation_sigmoid),
    Neural_output(64, 1, activation_sigmoid),
]

Neural_net = Neural_net(layers)

# (train_x, train_y), (test_x, test_y) = load_dataset()
# train_x = fix_dataset_array(train_x)
# train_y = fix_dataset_array(train_y)
train_x = np.array(
    [
        [1, 1, 1, 1],
        [0, 0, 0, 0],
        [1, 0, 0, 0],
        [0, 0, 0, 1],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
    ]
)
train_y = np.array([[1], [0], [1], [1], [0], [0]])

for i in range(5000):
    loss = Neural_net.train(train_x, train_y)
    if (i % 1000) == 0:
        print(loss)

print(Neural_net.think(train_x[1])[-1])