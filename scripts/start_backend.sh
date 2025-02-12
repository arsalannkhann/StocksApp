#!/bin/bash
echo "Starting Backend Server..."

cd /Users/arsalankhan/Documents/RESEARCH/StocksApp/backend
source venv/bin/activate
export PYTHONPATH=$(pwd)
python app.py