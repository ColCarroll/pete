import os
from pete import Broadcaster, Task

TEST_DIR = os.path.dirname(os.path.abspath(__file__))


class GatheringBroadcaster(Broadcaster):
    name = 'gathering broadcaster'

    def __init__(self):
        self.messages = []

    def send(self, messages):
        self.messages += messages


class NamedTask(Task):
    name = 'named task'

    def __init__(self):
        self.will_run = True
        self.run_count = 0

    def should_run(self):
        return self.will_run

    def run(self):
        self.run_count += 1
        return ["{0.name} {0.run_count}".format(self)]
