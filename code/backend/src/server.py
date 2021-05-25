from flask import Flask, send_from_directory
from flask_jwt_extended import JWTManager
from flask_mongoengine import MongoEngine

import api
import settings
from database import configure

server = Flask(__name__)

settings.load(server)

MongoEngine(server)
JWTManager(server)

api.register(server)


@server.route('/', defaults={'path': 'index.html'})
@server.route('/<path:path>')
def send_file(path):
    return send_from_directory("../../frontend/public", path)


configure.initialize()

if __name__ == "__main__":
    server.run(debug=True, host="0.0.0.0")
