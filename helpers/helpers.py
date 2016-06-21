import os


def touch(filename):
    """Touch a file, updating when it was last modified"""
    flags = os.O_CREAT | os.O_APPEND
    with os.fdopen(os.open(filename, flags=flags, mode=0o666)) as f:
        os.utime(f.fileno() if os.utime in os.supports_fd else filename)


def get_modified_time(filepath):
    """Get the time the filepath was last modified"""
    return os.stat(filepath).st_mtime
