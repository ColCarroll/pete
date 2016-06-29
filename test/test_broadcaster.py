import os
import time
import unittest

from broadcaster import Broadcaster, SQLiteBroadcaster


class TestBroadcaster(unittest.TestCase):
    def test_must_define_send(self):

        #  Can define an empty class, but not instantiate
        class EmptyBroadcaster(Broadcaster):
            pass
        with self.assertRaises(TypeError):
            EmptyBroadcaster()

        # Once we define a send method, things go fine
        EmptyBroadcaster.send = lambda x: None


class SampleSQLiteBroadcaster(SQLiteBroadcaster):
    # TODO: use a tempfile
    database = '__test_db.db'
    table = 'test_table'
    columns = [
        ('message_group', 'INT'),
        ('timestamp', 'FLOAT'),
        ('message_number', 'INT'),
        ('message', 'TEXT')
    ]

    def get_last_group_sent(self):
        query = "SELECT MAX(message_group) FROM {table}".format(table=self.table)
        with self.get_connection() as connection:
            last_group = self.query_single_row(connection, query)[0]
        if last_group is None:
            return -1
        else:
            return last_group

    def get_messages_sent(self):
        with self.get_connection() as connection:
            return self.row_count(connection)

    def send(self, messages):
        message_group = self.get_last_group_sent() + 1
        db_messages = []
        for message_number, message in enumerate(messages):
            db_messages.append((
                message_group,
                time.time(),
                message_number,
                message
            ))
        with self.get_connection() as connection:
            self.insert_rows(connection, db_messages)


class TestDBBroadcaster(unittest.TestCase):
    def setUp(self):
        self.broadcaster = SampleSQLiteBroadcaster()

    def tearDown(self):
        if os.path.exists(self.broadcaster.database):
            os.remove(self.broadcaster.database)

    def test_create_table(self):
        # Initializing broadcaster automatically creates the file
        os.remove(self.broadcaster.database)
        self.assertFalse(os.path.exists(self.broadcaster.database))

        with self.broadcaster.get_connection() as connection:
            self.broadcaster.create_table(connection)
        self.assertTrue(os.path.exists(self.broadcaster.database))

    def test_insert_row(self):
        with self.broadcaster.get_connection() as connection:
            self.broadcaster.insert_row(connection, (0, 0.0, 0, 'hello'))
        with self.broadcaster.get_connection() as connection:
            self.assertEqual(self.broadcaster.row_count(connection), 1)

    def test_insert_rows(self):
        rows = [(j, float(j), j, '{}. hello'.format(j)) for j in range(10)]
        with self.broadcaster.get_connection() as connection:
            self.broadcaster.insert_rows(connection, rows)
        with self.broadcaster.get_connection() as connection:
            self.assertEqual(self.broadcaster.row_count(connection), len(rows))

    def test_send(self):
        # These tests are particular to the sample broadcaster

        # Make sure empty to start
        with self.broadcaster.get_connection() as connection:
            self.assertEqual(self.broadcaster.row_count(connection), 0)

        message_stream = [
            ["message {} of {}".format(message_number, message_group)
                for message_number in range(message_group + 1)]
            for message_group in range(5)]

        messages_sent = 0
        for message_group, messages in enumerate(message_stream):
            # Confirm data persists between different broadcasters
            broadcaster = SampleSQLiteBroadcaster()
            broadcaster.send(messages)
            messages_sent += len(messages)
            self.assertEqual(broadcaster.get_last_group_sent(), message_group)
            self.assertEqual(broadcaster.get_messages_sent(), messages_sent)
