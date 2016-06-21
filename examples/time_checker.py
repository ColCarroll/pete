from datetime import datetime

from task import Task


class TimeChecker(Task):
    def should_run(self):
        return True

    def run(self):
        return "It is now {}".format(datetime.now().strftime("%H:%M:%S"))
