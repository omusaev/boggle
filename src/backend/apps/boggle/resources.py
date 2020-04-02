import datetime

from flask_restful import Resource, reqparse, fields, marshal_with, abort

from apps.boggle.board import (
    CombinationGenerator, WordSequenceValidator, WordLengthValidator,
    WordRulesLengthException, WordRulesSequenceException,
    WordScoreCalculator, Dictionary, WordDictionaryValidator,
    WordDictionaryValidatorException
)

from apps.boggle.errors import ErrorCodes
from apps.boggle.helpers import get_combination_or_abort, get_game_or_abort
from apps.boggle.models import BoardCombination, Game

from core.models.database import add_data, commit_data
from core.tasks.config import get_task_manager, TaskTypes

from conf import settings

from logging import getLogger

logger = getLogger(__name__)


new_game_parser = reqparse.RequestParser(bundle_errors=True)
new_game_parser.add_argument('player_name', required=False)
new_game_parser.add_argument('combination_id', dest='combination_uuid',
                             required=False)

new_word_parser = reqparse.RequestParser(bundle_errors=True)
new_word_parser.add_argument('word', required=True)

games_list_parser = reqparse.RequestParser(bundle_errors=True)
games_list_parser.add_argument('combination_id', dest='combination_uuid',
                               required=True)


game_fields = {
    'id': fields.String(attribute='uuid'),
    'combination_id': fields.String(attribute='board_combination.uuid'),
    'letters': fields.List(fields.String, attribute='board_combination.letters'),
    'player_name': fields.String,
    'created_at': fields.DateTime(dt_format='rfc822'),
    'found_words': fields.List(fields.Nested({
        'word': fields.String,
        'score': fields.Integer,
        'path': fields.List(fields.Integer)
    })),
    'final_score': fields.Integer,
}

games_list_fields = {
    'games': fields.List(fields.Nested({
        'player_name': fields.String,
        'final_score': fields.Integer,
    }))
}

combination_fields = {
    'id': fields.String(attribute='combination.uuid'),
    'letters': fields.List(fields.String, attribute='combination.letters'),
    'words': fields.List(fields.Nested({
        'word': fields.String,
        'path': fields.List(fields.Integer)
    }))
}


class GameListResource(Resource):

    @marshal_with(game_fields)
    def post(self):
        args = new_game_parser.parse_args()

        player_name = args.get('player_name')
        combination_uuid = args.get('combination_uuid')

        logger.debug('Received request for a new game with args: %s', args)

        if combination_uuid:
            combination = get_combination_or_abort(combination_uuid)
        else:
            letters = CombinationGenerator().new()
            combination = BoardCombination(letters=letters, words={})

            add_data(combination)

        new_game = Game(
            board_combination=combination,
            player_name=player_name,
            found_words=[],
            final_score=0
        )

        add_data(new_game)
        commit_data()

        if not new_game.board_combination.words:
            get_task_manager().async_task(TaskTypes.SOLVE_BOGGLE).send({
                'combination_id': new_game.board_combination.id,
            })

        return new_game, 201

    @marshal_with(games_list_fields)
    def get(self):
        args = games_list_parser.parse_args()
        combination_uuid = args['combination_uuid']

        combination = get_combination_or_abort(combination_uuid)

        return {'games': combination.games}


class GameResource(Resource):

    @marshal_with(game_fields)
    def get(self, game_uuid):
        game = get_game_or_abort(game_uuid)

        return game

    def delete(self, game_uuid):
        Game.query.filter_by(uuid=game_uuid).delete()
        commit_data()

        return '', 204

    @marshal_with(game_fields)
    def post(self, game_uuid):
        args = new_word_parser.parse_args()
        new_word = args['word'].upper()

        game = get_game_or_abort(game_uuid)

        logger.debug('Received request for new a word with args: %s', args)

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
        # first of all, let's check if have added the word already or not
        if new_word in (word['word'] for word in game.found_words):
            abort(
                400,
                error_message='The word has been added already',
                error_code=ErrorCodes.WORD_HAS_BEEN_ADDED_ALREADY
            )
        # the next cheapest validation is length validation
        length_validator = WordLengthValidator()

        try:
            path = length_validator.validate(new_word)
        except WordRulesLengthException as e:
            abort(
                400,
                error_message=str(e),
                error_code=ErrorCodes.INCORRECT_LENGTH
            )

        # ok, let's check the combination, maybe the background boggle
        # solver has solved it already
        if game.board_combination.words:
            word = game.board_combination.words.get(new_word)

            if word:
                logger.debug('Found the word in combination.words')
                return word['path']

        # ok, background solver is still working or the word hasn't been found
        # by it. If it's not in the combination.words it's either a fake word
        # or does not exist on the board, so we have to check both here
        sequence_validator = WordSequenceValidator(
            game.board_combination.letters
        )

        try:
            path = sequence_validator.validate(new_word)
        except WordRulesSequenceException as e:
            abort(
                400,
                error_message=str(e),
                error_code=ErrorCodes.INCORRECT_SEQUENCE
            )

        # ok, the sequence is present on the board, let's check
        # if it's a real word
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


class CombinationResource(Resource):

    @marshal_with(combination_fields)
    def get(self, combination_uuid):
        combination = get_combination_or_abort(combination_uuid)

        data = {
            'combination': combination,
            'words': [{'word': w, 'path': v['path']}
                      for w, v in combination.words.items()]
        }

        return data
