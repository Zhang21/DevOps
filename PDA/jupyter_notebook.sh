#!/bin/bash


jupyter notebook --no-browser --notebook-dir=/home/zhang/github/DevOps/PDA/tmp --ip=192.168.31.119 --port=8888 >/var/log/notebook.log 2>&1 &

