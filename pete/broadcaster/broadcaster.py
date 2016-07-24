from abc import ABCMeta, abstractmethod, abstractproperty
import json
import os
import sqlite3
import time

from .. import db
from .. import petemail


class Broadcaster(object, metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractproperty
    def name(self):
        """Name for the broadcaster"""
        return None

    @abstractmethod
    def send(self, messages):
        pass


class SQLiteBroadcaster(db.DBMixin, Broadcaster):
    """Parent class for SQLite broadcasters"""
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


class BasicSQLiteBroadcaster(SQLiteBroadcaster):
    columns = [
        ('message_group', 'INT'),
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

    def get_last_group_sent(self):
        query = "SELECT MAX(message_group) FROM {table}".format(table=self.table)
        with self.get_connection() as connection:
            last_group, = self.query_single_row(connection, query)
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


class BasicEmailBroadcaster(petemail.EmailMixin, Broadcaster):
    def send(self, messages):
        for message in messages:
            message_dict = json.loads(message)
            self.send_message(message_dict)
