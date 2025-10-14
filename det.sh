#!/bin/bash

echo "[1/4]  receiving..."
python CLIENT.py || { echo "error"; exit 1; }

echo "[2/4] detecting..."
python det_atlas.py || { echo "error"; exit 1; }

echo "[3/4] visualising..."
python vis.py || { echo "error"; exit 1; }

echo "[4/4] sending..."
python SERVER.py || { echo "initate.py 执行失败"; exit 1; }

firefox vis/pyvis/seq_graph_testing_preprocessed_logs_S4-CVE-2017-0199_windows_py.dot.txt.html

echo "finish"
