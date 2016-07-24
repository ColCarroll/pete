from abc import ABCMeta, abstractmethod, abstractproperty
import os
import sqlite3
import time

from .. import db


class Task(metaclass=ABCMeta):

    @abstractproperty
    def name(self):
        """Name for the task"""
        pass
        
    @abstractmethod
    def should_run(self):
        """Check whether the function should run.  Should be fast."""
        pass

    @abstractmethod
    def run(self):
        """Run the task and return a list of strings."""
        pass


class SQLiteTask(db.DBMixin, Task):
    host = None
    user = None
    password = None
    format_mark = "?"

    def __init__(self, *args, **kwargs):
        if not os.path.exists(self.database):
            with self.get_connection() as connection:
                self.create_table(connection)
        super().__init__(*args, **kwargs)

    def get_connection(self):
        """Get configured sqlite connection"""
        return sqlite3.connect(self.database)


class BasicSQLiteTask(SQLiteTask):
    columns = [
        ('timestamp', 'FLOAT'),
        ('message_number', 'INT'),
        ('message', 'TEXT')
    ]

    @abstractproperty
    def database(self):
        pass

    @abstractproperty
    def table(self):
        pass

    def get_last_message_number_sent(self):
        query = "SELECT MAX(message_number) FROM {table}".format(table=self.table)
        with self.get_connection() as connection:
            last_message, = self.query_single_row(connection, query)
        if last_message is None:
            return -1
        else:
            return last_message

    def register_message(self, message):
        message_number = self.get_last_message_number_sent()
        with self.get_connection() as connection:
            self.insert_row(connection, (time.time(), message_number + 1, message))

    def time_since_last_message(self):
        query = "SELECT MAX(timestamp) FROM {table}".format(table=self.table)
        with self.get_connection() as connection:
            last_timestamp, = self.query_single_row(connection, query)
        if last_timestamp is None:
            return time.time()
        else:
            return time.time() - last_timestamp

    def is_message_new(self, message):
        query = "SELECT COUNT(*) FROM {table} WHERE message = ?".format(table=self.table)
        with self.get_connection() as connection:
            count, = self.query_single_row(connection, query, (message,))
        return count == 0
