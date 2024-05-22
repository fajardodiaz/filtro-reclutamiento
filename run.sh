#!/bin/bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
nohup gunicorn --config gunicorn_config.py main:app &