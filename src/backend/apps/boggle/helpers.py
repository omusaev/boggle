from flask_restful import abort

from apps.boggle.errors import ErrorCodes
from apps.boggle.models import BoardCombination, Game


def get_combination_or_abort(combination_uuid):
    combination = BoardCombination.query. \
        filter_by(uuid=combination_uuid).first()

    if not combination:
        abort(
            400,
            error_message='Combination with id {} does not exist'.
                format(combination_uuid),
            error_code=ErrorCodes.COMBINATION_DOES_NOT_EXIST
        )

    return combination


def get_game_or_abort(game_uuid):
    game = Game.query.filter_by(uuid=game_uuid).first()

    if not game:
        abort(
            400,
            error_message='Game with id {} does not exist'.
                format(game_uuid),
            error_code=ErrorCodes.GAME_DOES_NOT_EXIST
        )

    return game
