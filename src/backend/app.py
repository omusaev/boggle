from flask import Flask
from flask_restful import Api

from apps.boggle.resources import Game, GameList

from core.models.database import init_db

import conf.settings as settings


init_db(settings.DATABASE)

app = Flask(__name__)
api = Api(app)

api.add_resource(GameList, '/games')
api.add_resource(Game, '/games/<game_uuid>')


if __name__ == '__main__':
    # not for production
    app.run(debug=settings.DEBUG, host='0.0.0.0')
