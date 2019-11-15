#!/bin/bash
# Author: Arjan de Haan (Vepnar)
# Script to move a python file easily to the raspberry pi and execute it

scp __hide__/* pi@192.168.10.46:~/testing/;
echo 'Uploading done...';
ssh -t pi@192.168.10.46 'sudo python3.7 ~/testing/main.py';

