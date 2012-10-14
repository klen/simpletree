from django.db import connection, transaction


def commit_raw_sql(func):
    """ Execute the query returns.
    """
    def wrapper(instance, write=True):
        sql = func(instance)
        cursor = connection.cursor()
        cursor.execute(sql)
        if write:
            transaction.commit_unless_managed()
    return wrapper
