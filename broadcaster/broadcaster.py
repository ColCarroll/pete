from abc import ABCMeta, abstractmethod, abstractproperty


class Broadcaster(metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def send(self, messages):
        pass


class DBBroadcaster(Broadcaster, metaclass=ABCMeta):
    columns = []

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
