from datetime import datetime

from pete.task import Task


class TimeChecker(Task):
    name = 'time checker task'
    
    def should_run(self):
        return True

    def run(self):
        return ["It is now {}".format(datetime.now().strftime("%H:%M:%S"))]
