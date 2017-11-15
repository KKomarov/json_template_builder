import os
from contextlib import contextmanager


@contextmanager
def pushd(new_path):
    old_path = os.getcwd()
    new_path = os.path.dirname(os.path.realpath(new_path))
    os.chdir(new_path)
    try:
        yield
    finally:
        os.chdir(old_path)
