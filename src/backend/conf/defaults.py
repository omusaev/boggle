import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))

LOGGING_LEVEL = 'ERROR'

FLASK = dict(
    SECRET_KEY=os.getenv('SECRET_KEY', 'secret'),
    FILE_STORAGE='/tmp/file_storage',
    DEBUG=False
)

DATABASE = {
    'sqlalchemy.url': "sqlite:///{}/data/boggle.db".format(ROOT_DIR)
}
