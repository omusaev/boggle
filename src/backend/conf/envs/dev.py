from conf.defaults import FLASK, ROOT_DIR

LOGGING_LEVEL = 'DEBUG'
FLASK['DEBUG'] = True

DATABASE = {
    'sqlalchemy.url': "sqlite:///{}/data/boggle.db".format(ROOT_DIR)
}
