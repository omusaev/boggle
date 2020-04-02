from kombu import Message

from apps.boggle.board import (
    Dictionary, WordSequenceValidator, WordRulesException, WordLengthValidator,
)
from apps.boggle.models import BoardCombination
from conf import settings
from core.tasks.consumer import BaseConsumer
from core.models.database import add_data

from logging import getLogger


logger = getLogger(__name__)


class BoggleSolverJob(BaseConsumer):

    def process_message(self, message: Message):
        data = message.payload
        combination_id = data['combination_id']

        combination = BoardCombination.query.get(combination_id)

        letters = combination.letters
        sequence_validator = WordSequenceValidator(combination=letters)
        length_validator = WordLengthValidator()
        dictionary = Dictionary(settings.BOGGLE_DICTIONARY_PATH)

        found_words = {}

        for word in dictionary.words:
            try:
                length_validator.validate(word)
                path = sequence_validator.validate(word)
                found_words[word] = {'path': path}
            except WordRulesException:
                pass

        logger.debug('Letters: %s', letters)
        logger.debug('Found words (%s), %s', len(found_words), found_words)

        combination.words = found_words

        add_data(combination, commit=True)
