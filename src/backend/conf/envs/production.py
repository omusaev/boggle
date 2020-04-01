import os

DATABASE = {
    'sqlalchemy.url': os.getenv('DB_CONNECTION_URL')
}
