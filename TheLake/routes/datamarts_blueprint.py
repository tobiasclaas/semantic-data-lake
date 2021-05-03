#coding: utf-8
from apis.datamartsApi import DatamartPreviewApi, DatamartSaveApi, DatamartSessionApi
from flask import Blueprint
from flask_restful import Api


DATAMARTS_BLUEPRINT = Blueprint('datamarts', __name__)

routes = ['/datamarts/session']
Api(DATAMARTS_BLUEPRINT).add_resource(
    DatamartSessionApi, *routes,
)

routes = ['/datamarts/preview']
Api(DATAMARTS_BLUEPRINT).add_resource(
    DatamartPreviewApi, *routes,
)

routes = ['/datamarts/save']
Api(DATAMARTS_BLUEPRINT).add_resource(
    DatamartSaveApi, *routes,
)