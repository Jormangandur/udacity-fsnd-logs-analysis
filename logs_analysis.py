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
    cursor.execute('''SELECT title, views FROM top_views LIMIT 3;''')
    result = cursor.fetchall()
    return result


@db_wrap
def top_3_authors(cursor):
    cursor.execute('''SELECT DISTINCT name,
                      sum(views) AS views
                      FROM top_views JOIN authors
                      ON (top_views.author = authors.id)
                      GROUP BY name
                      ORDER BY views DESC
                      LIMIT 3;''')
    result = cursor.fetchall()
    return result


top_articles = top_3_articles()
top_authors = top_3_authors()
print "The top 3 articles are:"
for article in top_articles:
    print " \"{0}\" - {1} views".format(article[0], article[1])


@db_wrap
def request_errors:
    pass


print "The top 3 authors are:"
for author in top_authors:
    print " {0} - {1} views".format(author[0], author[1])
