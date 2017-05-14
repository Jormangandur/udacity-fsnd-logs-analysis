#!/usr/bin/env python3

from functools import wraps
import psycopg2


def db_wrap(func):
    '''Wrap function in PostgreSQL transaction.

    Connects to database, creates a cursor, begins transaction, executes
    function then closes connection.
    Wrapped function needs cursor as first arg - other are preserved.

    Args:
        func: function to wrap with first argument as cursor
    '''
    @wraps(func)
    def connected_func(*args, **kwargs):
        conn = connect()
        c = conn.cursor()
        try:
            c.execute("BEGIN")
            transaction = func(c, *args, **kwargs)  # Pass cursor to func
            conn.commit()
        except:
            conn.rollback()  # Prevent any incorrect transactions on any error
            raise
        finally:
            c.close()
            conn.close()
        return transaction
    return connected_func


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect(dbname="news")


@db_wrap
def top_3_articles(cursor):
    """Gets the top 3 most viewed articles of all time.

    Returns:
        List of tuples in form (article_title, views)
    """
    cursor.execute("SELECT title, views FROM top_views LIMIT 3;")
    result = cursor.fetchall()
    return result


@db_wrap
def top_3_authors(cursor):
    """Gets the top 3 most viewed authors of all time.

    Returns:
        List of tuples in form (author_name, views)
    """
    cursor.execute('''SELECT DISTINCT name,
                      sum(views) AS views
                      FROM top_views JOIN authors
                      ON (top_views.author = authors.id)
                      GROUP BY name
                      ORDER BY views DESC
                      LIMIT 3;''')
    result = cursor.fetchall()
    return result


@db_wrap
def large_request_errors(cursor):
    """Gets any day with > 1 percent HTTP request errors.

    Returns:
        List of tuples in form (date, error_percentage)
    """
    cursor.execute('''SELECT day, error_percent
                      FROM request_stats
                      WHERE error_percent > 1
                      ORDER BY error_percent DESC;''')
    result = cursor.fetchall()
    return result


top_articles = top_3_articles()
top_authors = top_3_authors()
large_request_errors = large_request_errors()

print("The top 3 articles are:")
for article in top_articles:
    print("\"{0}\" - {1} views".format(article[0], article[1]))
print("The top 3 authors are:")
for author in top_authors:
    print("{0} - {1} views".format(author[0], author[1]))
print("Days with > 1% HTTP request errors are:")
for day in large_request_errors:
    print("{0} - {1}%".format(day[0], day[1]))
