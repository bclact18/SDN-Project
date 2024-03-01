@echo off
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
echo Requirements installed, run run.bat to start
pause