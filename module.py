import pygments
import sys

def inVenv():
    return sys.prefix != sys.base_prefix

def printpygments():
    if (inVenv()):
        print("I am a module in the venv")
    print(f'This is called from a module, pygments version {pygments.__version__}')