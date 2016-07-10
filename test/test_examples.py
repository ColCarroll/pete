import unittest
from unittest.mock import patch

from pete.examples import time_to_string_runner


class MockPrint(object):
    def __init__(self):
        self.messages = []

    def __call__(self, *args, **kwargs):
        self.messages.extend(args)


class TestExamples(unittest.TestCase):

    def test_example_runner(self):
        runner = time_to_string_runner()
        # Capture print, make sure
        with patch('builtins.print', MockPrint()) as mock_print:
            # Tick the task runner a few times, and make sure all the messages get mock printed
            for j in range(10):
                self.assertEqual(len(mock_print.messages), j)
                for message in mock_print.messages:
                    self.assertIn('It is now ', message)
                runner._tic()
