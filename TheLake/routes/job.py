#coding: utf-8
from flask import Blueprint
from flask_restful import Api

from apis.job import Job

JOB_BLUEPRINT = Blueprint("job", __name__)
routes = ['/job','/job/<uid>',]
Api(JOB_BLUEPRINT).add_resource(
    Job, *routes,
)