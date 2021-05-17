from flask import Flask, Blueprint
from api import blueprints


def register(server: Flask):
    for blueprint in vars(blueprints).values():
        if isinstance(blueprint, Blueprint):
            server.register_blueprint(blueprint, url_prefix="")
