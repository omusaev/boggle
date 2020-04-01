from conf.defaults import FLASK

LOGGING_LEVEL = 'INFO'
FLASK['DEBUG'] = True

# in memory DB
DATABASE = {
    'sqlalchemy.url': 'sqlite://'
}
