from flask import Flask
from flask_restful import Api

from core.models.database import init_db

import conf.settings as settings


app = Flask(__name__)
api = Api(app)

init_db(settings.DATABASE)


if __name__ == '__main__':
    # not for production
    app.run(debug=settings.DEBUG, host='0.0.0.0')
