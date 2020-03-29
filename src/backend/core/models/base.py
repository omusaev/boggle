import uuid

from sqlalchemy.ext.declarative import declarative_base

from core.models.database import db_session

Base = declarative_base()

# Set the query property for the models
Base.query = db_session.query_property()


def get_base_for_migrations():
    # we have to import all models here to use auto generation of migrations feature
    from apps.boggle.models import BoardCombination, Game

    return Base


def generate_uuid():
    return uuid.uuid4().hex
