set AVANGO_DIR=C:\Data\Repositories\vs2017\avango
set Path=%Path%;%AVANGO_DIR%\lib\Release;
set PYTHONPATH=%PYTHONPATH%;%AVANGO_DIR%\lib\python3.5;%AVANGO_DIR%\lib\python3.5\avango\daemon;%AVANGO_DIR%\examples

start "avango" cmd /K python daemon.py
start "avango" cmd /K python main.py