from flask_restful import Resource, reqparse, fields, marshal_with, abort

from apps.boggle.board import CombinationGenerator
from apps.boggle.models import BoardCombination, Game

from core.models.database import add_data, commit_data


new_game_parser = reqparse.RequestParser(bundle_errors=True)
new_game_parser.add_argument('player_name', required=False)
new_game_parser.add_argument('combination_id', required=False)

new_game_fields = {
    'uuid': fields.String,
    'combination_id': fields.String,
    'letters': fields.List(fields.String),
    'player_name': fields.String,
    'created_at': fields.String,
    'found_words': fields.List(fields.String),
    'final_score': fields.Integer,
}


class GameResource(Resource):

    def get(self, game_uuid):
        return {}

    def delete(self, game_uuid):
        return '', 204

    def put(self, game_uuid):
        return {}, 201


class GameListResource(Resource):

    @marshal_with(new_game_fields)
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

        game = {
            'uuid': new_game.uuid,
            'combination_id': combination.id,
            'letters': combination.letters,
            'player_name': new_game.player_name,
            'created_at': new_game.created_at,
            'found_words': new_game.found_words,
            'final_score': new_game.final_score
        }

        return game, 201
