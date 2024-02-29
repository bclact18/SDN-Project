import tensorflow
import module
import sys

def inVenv():
    return sys.prefix != sys.base_prefix


if __name__ == "__main__":
    if inVenv():
        print('I am main in a venv')
    print(f'This is the main file, tensorflow version {tensorflow.__version__}')
    module.printpygments()