import json
import os
import unittest
from unittest.mock import MagicMock

from pete import Broadcaster, BasicSQLiteBroadcaster, BasicEmailBroadcaster
from test_utils import TEST_DIR


class UsableSQLiteBroadcaster(BasicSQLiteBroadcaster):
    name = 'usable sqlite broadcaster'
    table = 'test_table'
    database = '__test_db'


class UsableEmailBroadcaster(BasicEmailBroadcaster):
    name = 'usable email broadcaster'
    email_config_filename = os.path.join(TEST_DIR, 'test_email_config.json')
    subject_formatter = '{subject}'
    message_formatter = '{message}'


def get_mock_smtp_server(host):
    mock_server = MagicMock()
    mock_server.host = host
    return mock_server


class TestEmailBroadcaster(unittest.TestCase):
    def setUp(self):
        self.broadcaster = UsableEmailBroadcaster()
        self.expected_config = json.load(open(UsableEmailBroadcaster.email_config_filename))

    def test_get_config(self):
        config = self.broadcaster._get_config()
        self.assertDictEqual(config, self.expected_config)

    def test_send_message(self):
        # TODO: remove this patch
        with unittest.mock.patch('smtplib.SMTP', autospec=True):
            self.broadcaster.send_message({"subject": "test", "message": "test"})


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
        self.broadcaster = UsableSQLiteBroadcaster()

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
            broadcaster = UsableSQLiteBroadcaster()
            broadcaster.send(messages)
            messages_sent += len(messages)
            self.assertEqual(broadcaster.get_last_group_sent(), message_group)
            self.assertEqual(broadcaster.get_messages_sent(), messages_sent)
