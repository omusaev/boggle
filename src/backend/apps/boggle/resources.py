import datetime

from flask_restful import Resource, reqparse, fields, marshal_with, abort

from apps.boggle.board import (
    CombinationGenerator, WordRulesValidator,
    WordRulesValidatorLengthException, WordRulesValidatorSequenceException,
    WordScoreCalculator, Dictionary, WordDictionaryValidator,
    WordDictionaryValidatorException
)
from apps.boggle.models import BoardCombination, Game

from core.models.database import add_data, commit_data
from conf import settings

from logging import getLogger

logger = getLogger(__name__)


new_game_parser = reqparse.RequestParser(bundle_errors=True)
new_game_parser.add_argument('player_name', required=False)
new_game_parser.add_argument('combination_id', required=False)

new_word_parser = reqparse.RequestParser(bundle_errors=True)
new_word_parser.add_argument('word', required=True)

word_fields = {
    'word': fields.String,
    'score': fields.Integer,
    'path': fields.List(fields.Integer)
}

game_fields = {
    'uuid': fields.String,
    'combination_id': fields.String(attribute='board_combination.id'),
    'letters': fields.List(fields.String, attribute='board_combination.letters'),
    'player_name': fields.String,
    'created_at': fields.DateTime(dt_format='rfc822'),
    'found_words': fields.List(fields.Nested(word_fields)),
    'final_score': fields.Integer,
}


class ErrorCodes:
    COMBINATION_DOES_NOT_EXIST = 'COMBINATION_DOES_NOT_EXIST'
    GAME_DOES_NOT_EXIST = 'GAME_DOES_NOT_EXIST'
    GAME_IS_FINISHED = 'GAME_IS_FINISHED'
    WORD_HAS_BEEN_ADDED_ALREADY = 'WORD_HAS_BEEN_ADDED_ALREADY'

    INCORRECT_LENGTH = 'INCORRECT_LENGTH'
    INCORRECT_SEQUENCE = 'INCORRECT_SEQUENCE'
    WORD_DOES_NOT_EXIST = 'WORD_DOES_NOT_EXIST'


class GameListResource(Resource):

    @marshal_with(game_fields)
    def post(self):
        args = new_game_parser.parse_args()

        player_name = args.get('player_name')
        combination_id = args.get('combination_id')

        logger.debug('Received request for a new game with args: %s', args)

        if combination_id:
            combination = BoardCombination.query.get(combination_id)

            if not combination:
                abort(
                    400,
                    error_message='Combination with id {} does not exist'.
                                  format(combination_id),
                    error_code=ErrorCodes.COMBINATION_DOES_NOT_EXIST
                )
        else:
            letters = CombinationGenerator().new()
            combination = BoardCombination(letters=letters)

            add_data(combination)

        new_game = Game(
            board_combination=combination,
            player_name=player_name,
            found_words=[],
            final_score=0
        )

        add_data(new_game)
        commit_data()

        return new_game, 201


class GameResource(Resource):

    def _get_game_or_abort(self, game_uuid):
        game = Game.query.filter_by(uuid=game_uuid).first()

        if not game:
            abort(
                400,
                error_message='Game with uuid {} does not exist'.
                    format(game_uuid),
                error_code=ErrorCodes.GAME_DOES_NOT_EXIST
            )

        return game

    @marshal_with(game_fields)
    def get(self, game_uuid):
        game = self._get_game_or_abort(game_uuid)

        return game

    def delete(self, game_uuid):
        Game.query.filter_by(uuid=game_uuid).delete()
        commit_data()

        return '', 204

    @marshal_with(game_fields)
    def post(self, game_uuid):
        args = new_word_parser.parse_args()
        new_word = args['word'].upper()

        game = self._get_game_or_abort(game_uuid)

        # TODO: definitely not the best way to check if the game has expired
        # considering the delays and network latency there might be +-2 seconds
        # difference. It's good enough for a casual game though so here we go
        elapsed = datetime.datetime.now() - game.created_at

        if elapsed > datetime.timedelta(seconds=settings.GAME_TTL):
            abort(
                400,
                error_message='The game is finished',
                error_code=ErrorCodes.GAME_IS_FINISHED
            )

        path = self._validate_new_word_and_abort_if_invalid(game, new_word)

        score = WordScoreCalculator().calc(new_word)

        game.found_words += [{'word': new_word, 'score': score, 'path': path}]
        game.final_score += score

        add_data(game, commit=True)

        return game, 201

    def _validate_new_word_and_abort_if_invalid(self, game, new_word):
        if new_word in (word['word'] for word in game.found_words):
            abort(
                400,
                error_message='The word has been added already',
                error_code=ErrorCodes.WORD_HAS_BEEN_ADDED_ALREADY
            )

        rules_validator = WordRulesValidator(game.board_combination.letters)

        try:
            path = rules_validator.validate(new_word)
        except WordRulesValidatorLengthException as e:
            abort(
                400,
                error_message=str(e),
                error_code=ErrorCodes.INCORRECT_LENGTH
            )
        except WordRulesValidatorSequenceException as e:
            abort(
                400,
                error_message=str(e),
                error_code=ErrorCodes.INCORRECT_SEQUENCE
            )

        dictionary = Dictionary(settings.BOGGLE_DICTIONARY_PATH)
        dictionary_validator = WordDictionaryValidator(dictionary)

        try:
            dictionary_validator.validate(new_word)
        except WordDictionaryValidatorException as e:
            abort(
                400,
                error_message=str(e),
                error_code=ErrorCodes.WORD_DOES_NOT_EXIST
            )

        return path
