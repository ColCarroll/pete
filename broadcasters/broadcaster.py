from abc import ABCMeta, abstractmethod


class Broadcaster(metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def send(self, messages):
        pass
