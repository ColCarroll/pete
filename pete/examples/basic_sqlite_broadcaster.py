import time

from pete.broadcaster import SQLiteBroadcaster


class BasicSQLiteBroadcaster(SQLiteBroadcaster):
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
