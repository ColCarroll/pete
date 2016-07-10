from pete.broadcaster import Broadcaster
from pete.task import Task


class GatheringBroadcaster(Broadcaster):
    def __init__(self):
        self.messages = []

    def send(self, messages):
        self.messages += messages


class NamedTask(Task):
    def __init__(self, name):
        self.name = name
        self.will_run = True
        self.run_count = 0

    def should_run(self):
        return self.will_run

    def run(self):
        self.run_count += 1
        return "{0.name} {0.run_count}".format(self)
