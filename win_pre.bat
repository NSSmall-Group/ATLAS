@echo off
echo [1/5]  preprocessing...
python preprocess.py
if errorlevel 1 goto error

echo [2/5]  graph generating...
python graph_generator.py
if errorlevel 1 goto error

echo [3/5]  graph reading...
python graph_reader.py
if errorlevel 1 goto error

echo [4/5]  initating...
python initate.py
if errorlevel 1 goto error

echo [5/5]  sending...
python SERVER.py
if errorlevel 1 goto error

echo finish!
goto end

:error
echo error
:end
pause
