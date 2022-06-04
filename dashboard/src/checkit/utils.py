import os
from contextlib import contextmanager

@contextmanager
def working_directory(path):
    """
    Temporarily change the current working directory.
    Usage:
    with working_directory(path):
        do_things()   # working in the given path
    do_other_things() # back to original path
    """
    current_directory=os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(current_directory)