import psycopg2
import psycopg2.extras


class Loader(object):
    """docstring for Loader"""
    def __init__(self, **kwargs):
        self.db_connect(**kwargs)

    def db_connect(self, **kwargs):
        """sets up a connection with a postgresql database using psycopg2"""
        conn = psycopg2.connect(**kwargs)
        self.cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def executeQuery(self, query_file, *args):
        """reads in file and executes it as a query"""
        with open(query_file, 'r') as f:
            query = f.read()
        self.cur.execute(query, args)

    def __iter__(self):
        return self

    def __next__(self):
        out = self.cur.fetchone()
        if out is None:
            raise StopIteration
        else:
            return out

    def next(self):
        out = self.__next__()
        if out is None:
            raise StopIteration
        else:
            return out
