import unittest

from pete.task import Task
from test_utils import NamedTask


class TestTask(unittest.TestCase):
    def test_must_supply_run(self):
        class NoRunTask(Task):
            def should_run(self):
                return True

        # Can't instantiate class without `run` method
        with self.assertRaises(TypeError):
            NoRunTask()

    def test_must_supply_should_run(self):
        class NoShouldRunTask(Task):
            def run(self):
                return 'Won\'t work.'

        # Can't instantiate class without `should_run` method
        with self.assertRaises(TypeError):
            NoShouldRunTask()

    def test_example_class(self):
        # Just confirming no TypeErrors
        NamedTask('just a test')
