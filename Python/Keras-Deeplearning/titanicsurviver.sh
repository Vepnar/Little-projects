py -m black titanicsurviver.py
docker run --gpus all -v -t  $PWD:/tmp -w /tmp tensorflow/tensorflow:latest-gpu python -m pip install pandas --user python titanicsurviver.py