import datetime

from sqlalchemy import (
    Column, DateTime, Integer, String, ForeignKey
)
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.mutable import MutableList, MutableDict

from core.models.base import Base, generate_uuid


class BoardCombination(Base):

    __tablename__ = 'board_combination'

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String(32), nullable=False, unique=True,
                  default=generate_uuid)
    letters = Column(JSON)
    words = Column(MutableDict.as_mutable(JSON))
    created_at = Column(DateTime, default=datetime.datetime.now)

    games = relationship('Game', backref=backref('board_combination'))


class Game(Base):

    __tablename__ = 'game'

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String(32), nullable=False, unique=True,
                  default=generate_uuid)
    player_name = Column(String(64), nullable=True)
    found_words = Column(MutableList.as_mutable(JSON))
    final_score = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.now)

    board_combination_id = Column(
        Integer,
        ForeignKey(
            BoardCombination.id,
            use_alter=True,
            name='board_combination_id',
            onupdate="CASCADE", ondelete="SET NULL"
        ),
        nullable=False
    )
