from flask import Flask
from flask_restful import Api

import conf.settings as settings

app = Flask(__name__)
api = Api(app)


if __name__ == '__main__':
    # not for production
    app.run(debug=settings.DEBUG, host='0.0.0.0')
