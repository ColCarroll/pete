from datetime import datetime

from . import Task
from helpers import mark_time


class TimeChecker(Task):
    def should_run(self):
        return True

    @mark_time
    def run(self):
        return "It is now {}".format(datetime.now().strftime("%H:%M:%S"))
