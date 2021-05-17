import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mongoengine import MongoEngine

import api
import settings
from business_logic.services.create_graph import Dashboard
from database import configure

server = Flask(__name__)

settings.load(server)

MongoEngine(server)
CORS(server, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
JWTManager(server)

dashboard = Dashboard()

api.register(server)

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
        return dashboard.create_graph(pathname.split("/dashboard/")[1])


@app.callback(
    Output('datatable-paging', 'data'), Input('datatable-paging', "page_current"),
    Input('datatable-paging', "page_size"), Input('datatable-paging', 'sort_by')
)
def update_table(page_current, page_size, sort_by):
    return dashboard.table_paging(page_current, page_size, sort_by)


@app.callback(
    Output('datatable-paging-sql', 'data'), Input('datatable-paging-sql', "page_current"),
    Input('datatable-paging-sql', "page_size"), Input('datatable-paging-sql', 'sort_by')
)
def update_table_sql(page_current, page_size, sort_by):
    return dashboard.table_paging_sql(page_current, page_size, sort_by)


@app.callback(
    Output('textarea-graph-output', 'children'), Input('textarea-graph-button', 'n_clicks'),
    State('textarea-graph', 'value')
)
def update_output(n_clicks, value):
    if n_clicks > 0:
        return dashboard.add_table(value)


@app.callback(
    Output('textarea-sql-output', 'children'), Input('textarea-sql-button', 'n_clicks'),
    State('textarea-sql', 'value')
)
def update_output_sql(n_clicks, value):
    if n_clicks > 0:
        return dashboard.run_sql(value)


@app.callback(
    Output('dataMart-output', 'children'), Input('input-dataMart-button', 'n_clicks'),
    State('input1DataMart', 'value'), State('input2DataMart', 'value'),
    State('input3DataMart', 'value'), State('input4DataMart', 'value'),
)
def save_datamart(n_clicks, input1_datamart, input2_datamart, input3_datamart, input4_datamart):
    if n_clicks > 0:
        return dashboard.save_data_mart(
            input1_datamart,
            input2_datamart,
            input3_datamart,
            input4_datamart
        )


configure.initialize()

if __name__ == "__main__":
    server.run(debug=True, host="0.0.0.0")
