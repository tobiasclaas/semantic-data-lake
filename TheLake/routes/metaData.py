#coding: utf-8
from flask import Blueprint
from flask_restful import Api

from apis.metaData import MetaData

METADATA_BLUEPRINT = Blueprint("metaData", __name__)
routes = ['/metaData','/metaData/<uid>',]
Api(METADATA_BLUEPRINT).add_resource(
    MetaData, *routes,
)