from flask_restful import Resource, reqparse, fields, marshal_with

from apps.boggle.board import CombinationGenerator
from apps.boggle.models import BoardCombination

from core.models.database import add_data, commit_data


new_game_parser = reqparse.RequestParser(bundle_errors=True)
new_game_parser.add_argument('player_name', required=False)
new_game_parser.add_argument('combination_id', required=False)

new_game_fields = {
    'uuid': fields.String,
    'combination_id': fields.String,
    'letters': fields.List(fields.String),
    'player_name': fields.String,
    'started_at': fields.String,
    'found_words': fields.List(fields.String),
    'final_score': fields.Integer,
}


class Game(Resource):

    def get(self, game_uuid):
        return {}

    def delete(self, game_uuid):
        return '', 204

    def put(self, game_uuid):
        return {}, 201


class GameList(Resource):

    @marshal_with(new_game_fields)
    def post(self):
        args = new_game_parser.parse_args()

        player_name = args.get('player_name')
        combination_id = args.get('combination_id')

        if combination_id:
            # TODO: get from db, raise an error if doesn't exist
            pass
        else:
            letters = CombinationGenerator().new()
            combination = BoardCombination(letters=letters)

            add_data(combination)
            commit_data()

        # TODO: create a new game, insert into DB
        game = {
            'uuid': '',
            'combination_id': combination.id,
            'letters': combination.letters,
            'player_name': player_name,
            'started_at': '',
            'found_words': [],
            'final_score': 123
        }

        return game, 201
