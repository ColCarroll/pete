from functools import wraps
import os

TIME_FILE_NAME = '.last_run'


def touch(fname):
    flags = os.O_CREAT | os.O_APPEND
    with os.fdopen(os.open(fname, flags=flags, mode=0o666)) as f:
        os.utime(f.fileno() if os.utime in os.supports_fd else fname)


def mark_time(function):
    directory = os.path.dirname(os.path.abspath(__file__))

    @wraps(function)
    def wrapped_function(*args, **kwargs):
        touch(os.path.join(directory, TIME_FILE_NAME))
        return function(*args, **kwargs)
    return wrapped_function
