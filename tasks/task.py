from abc import ABCMeta, abstractmethod


class Task(metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def should_run(self):
        """Check whether the function should run.  Should be fast."""
        pass


    @abstractmethod
    def run(self):
        """Run the task and return a string."""
        pass
