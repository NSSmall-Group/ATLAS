@echo off

echo [1/3]  receiving...
python CLIENT.py
if errorlevel 1 goto error

echo [2/3] detecting...
python det_atlas.py
if errorlevel 1 goto error

echo [2/3] visualisting...
python vis.py
if errorlevel 1 goto error

start vis/pyvis/seq_graph_testing_preprocessed_logs_S4-CVE-2017-0199_windows_py.dot.txt.html
echo finish

goto end

:error
echo error
:end
pause
