import time

from broadcasters import StringBroadcaster
from tasks import TimeChecker


class Runner(object):
    def __init__(self, tasks, broadcasters, timeout=60):
        self.tasks = tasks
        self.broadcasters = broadcasters
        self.timeout = timeout

    def run(self):
        """Run a single instance of all tasks"""
        messages = []
        for task in self.tasks:
            if task.should_run():
                task_message = task.run()
                if task_message:
                    messages.append(task_message)
        return messages

    def broadcast(self, message):
        for broadcaster in self.broadcasters:
            broadcaster.send(message)

    def main(self):
        while True:
            messages = self.run()
            if messages:
                self.broadcast(messages)
            time.sleep(self.timeout)


def main():
    runner = Runner(
        tasks=(TimeChecker(),),
        broadcasters=(StringBroadcaster(),),
        timeout=10
        )
    runner.main()

if __name__ == '__main__':
    main()
