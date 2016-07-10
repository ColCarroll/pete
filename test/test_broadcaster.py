import os
import unittest

from pete.broadcaster import Broadcaster
from pete.examples import BasicSQLiteBroadcaster


class TestBroadcaster(unittest.TestCase):
    def test_must_define_send(self):

        #  Can define an empty class, but not instantiate
        class EmptyBroadcaster(Broadcaster):
            pass
        with self.assertRaises(TypeError):
            EmptyBroadcaster()

        # Once we define a send method, things go fine
        EmptyBroadcaster.send = lambda x: None


class TestDBBroadcaster(unittest.TestCase):
    def setUp(self):
        self.broadcaster = BasicSQLiteBroadcaster()

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
        # These tests are particular to the basic sqlite broadcaster

        # Make sure empty to start
        self.assertEqual(self.broadcaster.get_messages_sent(), 0)

        message_stream = [
            ["message {} of {}".format(message_number, message_group)
                for message_number in range(message_group + 1)]
            for message_group in range(5)]

        messages_sent = 0
        for message_group, messages in enumerate(message_stream):
            # Confirm data persists between different broadcasters
            broadcaster = BasicSQLiteBroadcaster()
            broadcaster.send(messages)
            messages_sent += len(messages)
            self.assertEqual(broadcaster.get_last_group_sent(), message_group)
            self.assertEqual(broadcaster.get_messages_sent(), messages_sent)
