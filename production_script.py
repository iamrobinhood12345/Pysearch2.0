import os

def build_prod_string():

    production_db_url = os.environ["DATABASE_URL"]

    production_string = """###
    # app configuration
    # http://docs.pylonsproject.org/projects/pyramid/en/1.7-branch/narr/environment.html
    ###

    [app:pysearch]
    use = egg:pysearch

    pyramid.reload_templates = false
    pyramid.debug_authorization = false
    pyramid.debug_notfound = false
    pyramid.debug_routematch = false
    pyramid.default_locale_name = en

    ; sqlalchemy.url = postgres:///pysearch
    # sqlalchemy.url = postgres://@localhost:8888/pysearch
    sqlalchemy.url = {}

    [filter:paste_prefix]
    use = egg:PasteDeploy#prefix

    [pipeline:main]
    pipeline =
        paste_prefix
        pysearch

    [server:main]
    use = egg:waitress#main
    host = 0.0.0.0
    port = 6543

    ###
    # logging configuration
    # http://docs.pylonsproject.org/projects/pyramid/en/1.7-branch/narr/logging.html
    ###

    [loggers]
    keys = root, pysearch, sqlalchemy

    [handlers]
    keys = console

    [formatters]
    keys = generic

    [logger_root]
    level = WARN
    handlers = console

    [logger_pysearch]
    level = WARN
    handlers =
    qualname = pysearch

    [logger_sqlalchemy]
    level = WARN
    handlers =
    qualname = sqlalchemy.engine
    # "level = INFO" logs SQL queries.
    # "level = DEBUG" logs SQL queries and results.
    # "level = WARN" logs neither.  (Recommended for production systems.)

    [handler_console]
    class = StreamHandler
    args = (sys.stderr,)
    level = NOTSET
    formatter = generic

    [formatter_generic]
    format = %(asctime)s %(levelname)-5.5s [%(name)s:%(lineno)s][%(threadName)s] %(message)s
    """

    return production_string.format(production_db_url)


if __name__ == '__main__':
    with open('production.ini', 'w') as production:
        production.write(build_prod_string())