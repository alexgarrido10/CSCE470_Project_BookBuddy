#!/bin/bash

python3.12 -m venv bookbuddy
source bookbuddy/bin/activate
python3.12 -m pip install -U pip
pip install -r requirements10-29-24-6pm.txt
python -m spacy download en_core_web_sm