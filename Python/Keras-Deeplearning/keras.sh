py -m black keras.py
docker run -it -u $(id -u):$(id -g) --gpus all --rm -v $PWD:/tmp -w /tmp tensorflow/tensorflow:latest-gpu python keras.py