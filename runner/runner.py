import time


class Runner(object):
    def __init__(self, tasks, broadcasters, timeout=60):
        self.tasks = tasks
        self.broadcasters = broadcasters
        self.timeout = timeout

    def run(self):
        """Run a single instance of all tasks

        Returns:
            list of strings, messages from each task
        """
        messages = []
        for task in self.tasks:
            if task.should_run():
                task_message = task.run()
                if task_message:
                    messages.append(task_message)
        return messages

    def broadcast(self, messages):
        """Send a list of messages to all broadcasters.

        Args:
            messages: list of strings
        """
        for broadcaster in self.broadcasters:
            broadcaster.send(messages)

    def _tic(self):
        """Run and broadcast the tasks once."""
        messages = self.run()
        if messages:
            self.broadcast(messages)

    def main(self):
        """Run and broadcast the tasks forever."""
        while True:
            self._tic()
            time.sleep(self.timeout)
