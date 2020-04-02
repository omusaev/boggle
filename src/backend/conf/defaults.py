import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))

LOGGING_LEVEL = os.getenv('LOGGING_LEVEL', 'ERROR')

FLASK = dict(
    SECRET_KEY=os.getenv('SECRET_KEY', 'secret'),
    FILE_STORAGE='/tmp/file_storage',
    DEBUG=False
)

DATABASE = {
    'sqlalchemy.url': os.getenv('DB_CONNECTION_URL')
}

TASKS_BROKER_URL = os.getenv('TASKS_BROKER_URL')

GAME_TTL = 3 * 60  # 180 sec
BOGGLE_DICTIONARY_PATH = os.path.join(
    ROOT_DIR, 'apps/boggle/dictionary/collins_scrabble_words.txt'
)
