#!/bin/bash

echo "==========Welcome to the Bootstrap for this Speech Recognition Software==========="
echo "******* Commands understood *******"
echo "go home/ 'to <destination>'"
echo "hello world"
echo "More commands will be added soon....."
echo ""
echo "==================Initializing Environment==================="
virtualenv -p python3 $HOME/tmp/deepspeech-venv/
source $HOME/tmp/deepspeech-venv/bin/activate
pip3 install deepspeech

echo "=====Done!======="
echo "Starting Program..."
echo ""
sleep 1
python3 `pwd`/start_deep.py
