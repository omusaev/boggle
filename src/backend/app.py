from flask import Flask
from flask_restful import Api

from apps.boggle.resources import GameResource, GameListResource

from core.models.database import init_db

import conf.settings as settings


init_db(settings.DATABASE)

app = Flask(__name__)
api = Api(app)

api.add_resource(GameListResource, '/api/v1/games')
api.add_resource(GameResource, '/api/v1/games/<game_uuid>')


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')

    response.headers.add('Cache-Control', 'no-cache,no-store,must-revalidate')
    response.headers.add('Pragma', 'no-cache')
    response.headers.add('Expires', '0')

    return response


if __name__ == '__main__':
    # not for production
    app.run(debug=settings.DEBUG, host='0.0.0.0')
