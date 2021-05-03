#coding: utf-8
import os
import routes
from flask import *
from flask.blueprints import Blueprint
from flask_mongoengine import MongoEngine
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
from services.backup import backupDb
from pyspark.sql import *
from services.createGraph import Dashboard
from dash.dependencies import Input, Output, State
import script
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import psycopg2
import sys

server = Flask(__name__)

mapro_dev = os.environ.get("MAPRO_DEV")
if mapro_dev == "alex":
  server.config.from_object("configs.DevelopmentConfigAlex")
elif mapro_dev == "marcel":
  server.config.from_object("configs.DevelopmentConfigMarcel") 
elif mapro_dev == "robin":
  server.config.from_object("configs.DevelopmentConfigRobin")  
else:
  if os.environ.get("IN_DOCKER", False):
    server.config.from_object("configs.ProductionConfigDocker")
  else:
    server.config.from_object("configs.ProductionConfig")

db = MongoEngine(server)
jwt = JWTManager(server)
CORS(server, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
d = Dashboard()

if (server.config["DEBUG"] == False and server.config["TESTING"] == False):
  scheduler = BackgroundScheduler()
  scheduler.add_job(func=backupDb, trigger="interval", seconds=30)
  scheduler.start()

for blueprint in vars(routes).values():
  if isinstance(blueprint, Blueprint):
    server.register_blueprint(blueprint, url_prefix="")

app = dash.Dash(
    __name__,
    server=server,
    routes_pathname_prefix='/dashboard/',
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

app.layout = html.Div([dcc.Location(id='url', refresh=False), html.Div(id='page-content')])


@app.callback(
    dash.dependencies.Output('page-content', 'children'),
    [dash.dependencies.Input('url', 'pathname')]
)
def display_page(pathname):
  if "/dashboard/" not in pathname:
    pass
  else:
    return d.createGraph(pathname.split("/dashboard/")[1], server)


@app.callback(
    Output('datatable-paging', 'data'), Input('datatable-paging', "page_current"),
    Input('datatable-paging', "page_size"), Input('datatable-paging', 'sort_by')
)
def update_table(page_current, page_size, sort_by):
  return d.tablePaging(page_current, page_size, sort_by)

@app.callback(
    Output('datatable-paging-sql', 'data'), Input('datatable-paging-sql', "page_current"),
    Input('datatable-paging-sql', "page_size"), Input('datatable-paging-sql', 'sort_by')
)
def update_table_sql(page_current, page_size, sort_by):
  return d.tablePagingSQL(page_current, page_size, sort_by)


@app.callback(
    Output('textarea-graph-output', 'children'), Input('textarea-graph-button', 'n_clicks'),
    State('textarea-graph', 'value')
)
def update_output(n_clicks, value):
  if n_clicks > 0:
    return d.addTable(value)
  
@app.callback(
    Output('textarea-sql-output', 'children'), Input('textarea-sql-button', 'n_clicks'),
    State('textarea-sql', 'value')
)
def update_output_sql(n_clicks, value):
  if n_clicks > 0:
    return d.runSQL(value)

@app.callback(
    Output('dataMart-output', 'children'), Input('input-dataMart-button', 'n_clicks'),
    State('input1DataMart', 'value'), State('input2DataMart', 'value'),
    State('input3DataMart', 'value'), State('input4DataMart', 'value'),
)
def save_dataMart(n_clicks, input1DataMart, input2DataMart, input3DataMart, input4DataMart):
  if n_clicks > 0:
    return d.saveDataMart(input1DataMart,input2DataMart, input3DataMart, input4DataMart)


#--------------------------------------------------------------------------------------------------
# main
#--------------------------------------------------------------------------------------------------
if __name__ == '__main__':
  script.register(server)
  app.run_server(debug=True, host=server.config["HOST"], port=server.config["PORT"], threaded=True)
