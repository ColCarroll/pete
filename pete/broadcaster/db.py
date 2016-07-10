from abc import abstractproperty
import os
import sqlite3

from .broadcaster import Broadcaster


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
        """Get the number of rows in the table.

        Args:
            connection: Database connection

        Returns:
            Integer, number of rows in the table
        """
        query = "SELECT COUNT(*) FROM {table}".format(table=self.table)
        return self.query_single_row(connection, query)[0]

    def insert_row(self, connection, row):
        """Insert a row into the table.

        Args:
            connection: Database connection
            row: row data
        """
        formatters = ",".join([self.format_mark for _ in row])
        query = "INSERT INTO {table} values ({formatters})".format(
            table=self.table, formatters=formatters)
        connection.cursor().execute(query, row)

    def insert_rows(self, connection, rows):
        """Insert multiple rows into the table.

        Just a wrapper around `insert_row`.

        Args:
            connection: Database connection
            rows: iterator of row data
        """
        for row in rows:
            self.insert_row(connection, row)

    def query_single_row(self, connection, query, args=None):
        """Execute a query and return the first row.

        Args:
            connection: Database connection
            query: sql query to execute
            args: optional arguments to be passed to the query string

        Returns:
            single tuple of results
        """
        if args is None:
            args = []
        cur = connection.cursor()
        cur.execute(query, args)
        return cur.fetchone()


class SQLiteBroadcaster(DBBroadcaster):
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

