@echo off
python -m venv venv
call venv/Scripts/activate
pip install -r requirements.txt
echo Requirements installed, launch run.bat to run
pause