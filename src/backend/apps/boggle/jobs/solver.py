from kombu import Message

from apps.boggle.board import (
    Dictionary, WordRulesValidator, WordRulesValidatorException
)
from apps.boggle.models import Game
from conf import settings
from core.tasks.consumer import BaseConsumer
from core.models.database import add_data

from logging import getLogger


logger = getLogger(__name__)


class BoggleSolverJob(BaseConsumer):

    def process_message(self, message: Message):
        data = message.payload
        game_id = data['game_id']

        game = Game.query.get(game_id)
        letters = game.board_combination.letters
        validator = WordRulesValidator(combination=letters)
        dictionary = Dictionary(settings.BOGGLE_DICTIONARY_PATH)

        found_words = {}

        for word in dictionary.words:
            try:
                path = validator.validate(word)
                found_words[word] = {'path': path}
            except WordRulesValidatorException:
                pass

        logger.debug('Letters: %s', letters)
        logger.debug('Found words (%s), %s', len(found_words), found_words)

        game.board_combination.words = found_words

        add_data(game, commit=True)
