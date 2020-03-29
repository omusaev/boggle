from flask import Flask
from flask_restful import Api

from apps.boggle.resources import GameResource, GameListResource

from core.models.database import init_db

import conf.settings as settings


init_db(settings.DATABASE)

app = Flask(__name__)
api = Api(app)

api.add_resource(GameListResource, '/games')
api.add_resource(GameResource, '/games/<game_uuid>')


if __name__ == '__main__':
    # not for production
    app.run(debug=settings.DEBUG, host='0.0.0.0')
