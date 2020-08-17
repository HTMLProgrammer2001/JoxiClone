from flask import Flask, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import Config


app = Flask(__name__)
app.config.from_object(Config())

db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.errorhandler(404)
def notFound(e):
	return make_response('Not found')


import routes

if __name__ == '__main__':
	app.run(debug=True)