from abc import ABCMeta, abstractmethod


class Broadcaster(metaclass=ABCMeta):
    @abstractmethod
    def send(self, messages):
        pass
