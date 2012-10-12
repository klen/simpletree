from django.db import connection, transaction


def commit_raw_sql(func):
    """ Decorator for makes queries.
    """
    def wrapper(instance, write=True):
        sql = func(instance)
        cursor = connection.cursor()
        cursor.execute(sql)
        if write:
            transaction.commit_unless_managed()
    return wrapper
