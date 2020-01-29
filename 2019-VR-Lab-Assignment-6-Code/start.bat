set AVANGO_DIR=C:\Data\Repositories\avango
set Path=%Path%;%AVANGO_DIR%\lib\Release;
set PYTHONPATH=%PYTHONPATH%;%AVANGO_DIR%\lib\python3.5;%AVANGO_DIR%\lib\python3.5\avango\daemon;%AVANGO_DIR%\examples

:: kill all avango windows from last run
start /B kill.bat
ping -n 2 127.0.0.1 > NUL

start "avango" cmd /K python daemon.py
start "avango" cmd /K python main.py
