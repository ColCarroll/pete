import unittest

from pete.runner import Runner
from test_utils import NamedTask, GatheringBroadcaster


class TestRunner(unittest.TestCase):
    def setUp(self):
        self.run_task = NamedTask('Does run')
        self.no_run_task = NamedTask('Does not run')
        self.no_run_task.will_run = False
        self.broadcasters = [GatheringBroadcaster() for _ in range(3)]
        self.runner = Runner(
            tasks=[self.run_task, self.no_run_task],
            broadcasters=self.broadcasters)

    def test_run(self):
        messages = self.runner.run()
        self.assertEqual(self.run_task.run_count, 1)
        self.assertEqual(self.no_run_task.run_count, 0)
        self.assertEqual(len(messages), 1)

    def test_broadcast(self):
        messages = self.runner.run()

        # Nothing is broadcast yet
        for broadcaster in self.broadcasters:
            self.assertListEqual(broadcaster.messages, [])

        self.runner.broadcast(messages)

        # Now all broadcasters got the messages
        for broadcaster in self.broadcasters:
            self.assertListEqual(broadcaster.messages, messages)

    def test__tic(self):
        self.runner._tic()

        # Only one task ran
        self.assertEqual(self.run_task.run_count, 1)
        self.assertEqual(self.no_run_task.run_count, 0)
        for broadcaster in self.broadcasters:
            self.assertEqual(len(broadcaster.messages), 1)

        self.no_run_task.will_run = True
        self.runner._tic()

        # Both tasks ran
        self.assertEqual(self.run_task.run_count, 2)
        self.assertEqual(self.no_run_task.run_count, 1)
        for broadcaster in self.broadcasters:
            self.assertEqual(len(broadcaster.messages), 3)
