import os
import unittest

from pete import Task, BasicSQLiteTask
from test_utils import NamedTask


class UsableSQLiteTask(BasicSQLiteTask):
    table = 'test_task_table'
    database = '__test_db'
    name = 'usable sqlite task'

    def __init__(self, message):
        super().__init__()
        self.message = message

    def should_run(self):
        return True

    def run(self):
        self.register_message(self.message)
        return self.message


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
        NamedTask()


class TestSQLiteTask(unittest.TestCase):
    def setUp(self):
        self.message = 'test message'
        self.task = UsableSQLiteTask(self.message)

    def tearDown(self):
        if os.path.exists(self.task.database):
            os.remove(self.task.database)

    def test_run(self):
        self.task.run()
        with self.task.get_connection() as connection:
            self.assertEqual(self.task.row_count(connection), 1)

    def test_get_last_message_number_sent(self):
        for j in range(5):
            # create new task each loop
            task = UsableSQLiteTask(self.message)
            self.assertEqual(task.get_last_message_number_sent(), j - 1)
            task.run()

    def test_time_since_last_message(self):
        with unittest.mock.patch('time.time') as mock_time:
            mock_time.return_value = 1000
            self.assertEqual(self.task.time_since_last_message(), 1000)
            self.task.run()
            mock_time.return_value = 1010
            self.assertEqual(self.task.time_since_last_message(), 10)

    def test_is_message_new(self):
        self.assertTrue(self.task.is_message_new(self.message))
        self.task.run()
        self.assertFalse(self.task.is_message_new(self.message))
