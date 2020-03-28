from typing import Dict

from sqlalchemy import engine_from_config
from sqlalchemy.orm import scoped_session, sessionmaker

# Sqlalchemy scoped_session object. Use this object to interact with
# sqlalchemy, e.g. commit, add ...
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False))

# Holds the engine to make it available get_engine. Don't use
# this directly.
__db_engine = None


def reset_db() -> None:
    """Removes the current Session."""
    db_session.remove()


def get_engine():
    """Returns the sqlalchemy engine object.

    Only use this if you know what you are doing. Use :py:data:`db_session`
    wherever possible.

    :rtype: sqlalchemy.engine.Engine
    :raises AssertionError: if the engine was not initialized. Make sure to \
    call :py:func:`init_db` prior to this function.
    """
    assert __db_engine is not None
    return __db_engine


def init_db(config: Dict):
    """Initilizes the database.

    Use this function to setup the database. It creates the engine and binds it
    to the db_session. It returns the sqlalchemy engine, usually the engine should
    not be used. However, there might be reasons to do so e.g. to drop tables.

    :param config: Sqlalchemy config dictionary.
    :rtype: sqlalchemy.engine.Engine
    """
    global __db_engine
    # create the engine
    __db_engine = engine_from_config(config, convert_unicode=True)
    # bind the engine to the sessionmaker
    db_session.configure(bind=__db_engine)

    return __db_engine


def add_data(data) -> None:
    """Adds data to the database.

    Adds the data given as sqlalchemy data object to the session and then
    commits the changes. In effect this saves the changes to the database.

    :param data: The sqlalchemy data object to add.
    """
    db_session.add(data)
    db_session.commit()


def delete_data(data) -> None:
    """Delete data from the database.

    Mark given data as deleted and commit changes to the database.

    :param data: The sqlalchemy data object to add.
    """
    db_session.delete(data)
    db_session.commit()


def commit_data() -> None:
    """Commits session changes to database"""
    db_session.commit()
