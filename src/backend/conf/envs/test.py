from conf.defaults import FLASK

LOGGING_LEVEL = 'DEBUG'
FLASK['DEBUG'] = True

# in memory DB
DATABASE = {
    'sqlalchemy.url': 'sqlite://'
}
