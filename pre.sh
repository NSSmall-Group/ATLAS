#!/bin/bash

echo "[1/6] preprocessing..."
python preprocess.py || { echo "preprocess.py 执行失败"; exit 1; }

echo "[2/6] graph generating..."
python graph_generator.py || { echo "graph_generator.py 执行失败"; exit 1; }

echo "[3/6] graph_reading.py..."
python graph_reader.py || { echo "graph_reader.py 执行失败"; exit 1; }

echo "[4/6] initing..."
python initate.py || { echo "initate.py 执行失败"; exit 1; }

echo "[5/6] sending..."
python SERVER.py || { echo "initate.py 执行失败"; exit 1; }

echo "[6/6] waiting for result..."
python CLIENT.py || { echo "initate.py 执行失败"; exit 1; }

firefox vis/pyvis/seq_graph_testing_preprocessed_logs_S4-CVE-2017-0199_windows_py.dot.txt.html

echo "finish"
