from flask_restful import Resource


class Game(Resource):

    def get(self, game_uuid):
        return {}

    def delete(self, game_uuid):
        return '', 204

    def put(self, game_uuid):
        return {}, 201


class GameList(Resource):

    def post(self):
        return {}, 201
