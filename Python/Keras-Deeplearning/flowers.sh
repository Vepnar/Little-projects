py -m black flowers.py

docker run -it -u $(id -u):$(id -g) --gpus all --rm -v $PWD:/tmp -w /tmp tensorflow/tensorflow:latest-gpu python flowers.py