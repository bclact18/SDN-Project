source venv/bin/activate
PYTHON3_VENV_PATH=$(which python3)

sudo $PYTHON3_VENV_PATH main.py "$@"