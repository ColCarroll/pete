from abc import ABCMeta, abstractmethod, abstractproperty
import os
import sqlite3


class Broadcaster(metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def send(self, messages):
        pass


class DBBroadcaster(Broadcaster):
    @abstractproperty
    def host(self):
        return None

    @abstractproperty
    def database(self):
        return None

    @abstractproperty
    def user(self):
        return None

    @abstractproperty
    def password(self):
        return None

    @abstractproperty
    def table(self):
        return None

    @abstractproperty
    def columns(self):
        return None

    @abstractproperty
    def format_mark(self):
        return None

    def create_table(self, connection):
        """
        Override to provide code for creating the target table.

        By default it will be created using types (optionally) specified in columns.

        If overridden, use the provided connection object for setting up the table in order to
        create the table and insert data using the same transaction.
        """
        coldefs = ','.join('{name} {col_type}'.format(name=name, col_type=col_type)
                           for name, col_type in self.columns)
        query = "CREATE TABLE {table} ({coldefs})".format(table=self.table, coldefs=coldefs)
        connection.cursor().execute(query)

    def row_count(self, connection):
        query = "SELECT COUNT(*) FROM {table}".format(table=self.table)
        return self.query_single_row(connection, query)[0]

    def insert_row(self, connection, row_data):
        formatters = ",".join([self.format_mark for _ in row_data])
        query = "INSERT INTO {table} values ({formatters})".format(
            table=self.table, formatters=formatters)
        connection.cursor().execute(query, row_data)

    def insert_rows(self, connection, rows):
        for row in rows:
            self.insert_row(connection, row)

    def query_single_row(self, connection, query, args=None):
        if args is None:
            args = []
        cur = connection.cursor()
        cur.execute(query, args)
        return cur.fetchone()

    def query_iterator(self, connection, query, args=None):
        if args is None:
            args = []
        cur = connection.cursor()
        cur.execute(query, args)
        for row in cur:
            yield row


class SQLiteBroadcaster(DBBroadcaster):
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
        return sqlite3.connect(self.database)
