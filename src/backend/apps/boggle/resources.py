from flask_restful import Resource, reqparse, fields, marshal_with, abort

from apps.boggle.board import CombinationGenerator
from apps.boggle.models import BoardCombination, Game

from core.models.database import add_data, commit_data


new_game_parser = reqparse.RequestParser(bundle_errors=True)
new_game_parser.add_argument('player_name', required=False)
new_game_parser.add_argument('combination_id', required=False)

game_fields = {
    'uuid': fields.String,
    'combination_id': fields.String(attribute='board_combination.id'),
    'letters': fields.List(fields.String, attribute='board_combination.letters'),
    'player_name': fields.String,
    'created_at': fields.DateTime(dt_format='rfc822'),
    'found_words': fields.List(fields.String),
    'final_score': fields.Integer,
}


class GameListResource(Resource):

    @marshal_with(game_fields)
    def post(self):
        args = new_game_parser.parse_args()

        player_name = args.get('player_name')
        combination_id = args.get('combination_id')

        if combination_id:
            combination = BoardCombination.query.get(combination_id)

            if not combination:
                abort(
                    400,
                    error_message='Combination with id {} does not exist'.
                                  format(combination_id)
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

        add_data(combination)
        commit_data()

        return new_game, 201


class GameResource(Resource):

    def _get_game_or_abort(self, game_uuid):
        game = Game.query.filter_by(uuid=game_uuid).first()

        if not game:
            abort(
                400,
                error_message='Game with uuid {} does not exist'.
                    format(game_uuid)
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

    def put(self, game_uuid):
        return {}, 201
