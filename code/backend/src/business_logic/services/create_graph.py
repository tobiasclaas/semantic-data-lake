from business_logic.services.create_datamart import create_datamart
from business_logic.spark import SparkHelper
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash_table import DataTable
import uuid
from passlib.hash import pbkdf2_sha256 as sha256

from database.data_access import datamart_data_access, user_data_access


class Dashboard:
    PAGE_SIZE = 20
    dataframe_pandas = None
    dataframe = None
    datamart = None
    spark_helper = None
    df_datamart = None
    df_datamart_pandas = None

    def data_access(self, datamart_id):
        self.spark_helper = SparkHelper(f"graph_{uuid.uuid4()}")
        self.datamart = datamart_data_access.get_by_uid(datamart_id)
        self.dataframe = self.spark_helper.read_datamart(self.datamart)
        self.dataframe_pandas = self.dataframe.toPandas()

    def create_graph(self, datamart_id):
        self.spark_helper = SparkHelper(f"graph_{uuid.uuid4()}")
        self.datamart = datamart_data_access.get_by_uid(datamart_id)
        self.dataframe = self.spark_helper.read_datamart(self.datamart)
        self.dataframe_pandas = self.dataframe.toPandas()

        return html.Div(children=[
            html.Div(className='row',
                     style={'padding': 10},
                     id=datamart_id,
                     children=[
                         dbc.Col(html.Div(children=[
                             html.H1(datamart_id),
                             html.H2("Data"),
                             DataTable(
                                 id='datatable-paging',
                                 columns=[
                                     {"name": i, "id": i} for i in
                                     sorted(self.dataframe_pandas.columns)
                                 ],
                                 page_current=0,
                                 page_size=self.PAGE_SIZE,
                                 page_action='custom',
                                 sort_action='custom',
                                 sort_mode='single',
                                 sort_by=[]
                             ),
                         ]), width=12),
                         dbc.Col(html.Div(children=[
                             html.H2("SQL"),
                             dbc.Textarea(
                                 id='textarea-sql',
                                 placeholder='SELECT * FROM ViewName;',
                                 value='SELECT * FROM ViewName;',
                                 style={'width': '100%', 'height': 200, 'margin-bottom': 10},
                             ),
                             dbc.Button('Submit', id='textarea-sql-button', n_clicks=0),
                             html.Div(id='textarea-sql-output',
                                      style={'whiteSpace': 'pre-line', 'margin-top': 10,
                                             'margin-bottom': 10}),
                         ]), width=12),
                         dbc.Col(html.Div(children=[
                             html.H2("Create Own Charts"),
                             dcc.Markdown('''
                                    ### Documentation

                                    #### Create a Figure

                                    The dataframe are loaded with spark and transformed to a pandas dataframe. So we can use it with plotly. 

                                    The following Plotly pakages are imported: 
                                    ```python
                                    import dash
                                    import dash_html_components as html
                                    import dash_core_components as dcc
                                    import plotly.express as px
                                    import pandas as pd
                                    import plotly.graph_objects as go
                                    import dash_bootstrap_components as dbc
                                    import re
                                    from plotly.subplots import make_subplots
                                    from dash_table import DataTable
                                    ```

                                    If you want to see the figure in a different tab you can call:
                                    - fig.show()

                                    #### Examples for Plotly Express

                                    ```python
                                    #Ordinary Least Square 
                                    df = px.data.tips()
                                    fig = px.scatter(
                                        df, x='total_bill', y='tip', opacity=0.65,
                                        trendline='ols', trendline_color_override='darkblue'
                                    )
                                    finishedFigure.append(fig)

                                    #Bubble chart
                                    df = px.data.gapminder()
                                    fig = px.scatter(df.query("year==2007"), x="gdpPercap", y="lifeExp",
                                              size="pop", color="continent",
                                                    hover_name="country", log_x=True, size_max=60)
                                    finishedFigure.append(fig)

                                    #Pie chart
                                    df = px.data.gapminder().query("year == 2007").query("continent == 'Europe'")
                                    df.loc[df['pop'] < 2.e6, 'country'] = 'Other countries' # Represent only large countries
                                    fig = px.pie(df, values='pop', names='country', title='Population of European continent')
                                    finishedFigure.append(fig)

                                    #Histogram
                                    df = px.data.tips()
                                    fig = px.histogram(df, x="total_bill")
                                    finishedFigure.append(fig)

                                    #Iris
                                    df = px.data.iris()
                                    fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species",
                                                    size='petal_length', hover_data=['petal_width'])
                                    finishedFigure.append(fig)
                                    ```
                                    '''),
                             dbc.Textarea(
                                 id='textarea-graph',
                                 placeholder='finishedFigure=[] #required\ndf=self.dfPandas #required\n#code\nfinishedFigure.append(fig) #required',
                                 value='finishedFigure=[] #required\ndf=self.dfPandas #required\n#code\nfinishedFigure.append(fig) #required',
                                 style={'width': '100%', 'height': 200, 'margin-bottom': 10},
                             ),
                             dbc.Button('Submit', id='textarea-graph-button', n_clicks=0),
                             html.Div(id='textarea-graph-output',
                                      style={'whiteSpace': 'pre-line', 'margin-top': 10,
                                             'margin-bottom': 10}),
                         ]), width=12),
                     ])
        ])

    def table_paging(self, page_current, page_size, sort_by):
        if len(sort_by):
            dff = self.dataframe_pandas.sort_values(
                sort_by[0]['column_id'],
                ascending=sort_by[0]['direction'] == 'asc',
                inplace=False
            )
        else:
            dff = self.dataframe_pandas
        return dff.iloc[
               page_current * page_size:(page_current + 1) * page_size
               ].to_dict('records')

    def table_paging_sql(self, page_current, page_size, sort_by):
        if len(sort_by):
            dff = self.df_datamart_pandas.sort_values(
                sort_by[0]['column_id'],
                ascending=sort_by[0]['direction'] == 'asc',
                inplace=False
            )
        else:
            dff = self.df_datamart_pandas
        return dff.iloc[
               page_current * page_size:(page_current + 1) * page_size
               ].to_dict('records')

    def add_table(self, value):
        lc = locals()
        gl = globals()
        fig = None
        try:
            exec(value, gl, lc)
        except Exception as e:
            return html.Div([
                dbc.Alert(str(e), color="danger"),
            ])
        ret = []
        for fig in lc["finishedFigure"]:
            ret.append(dcc.Graph(figure=fig))
        return html.Div(
            children=ret
        )

    def save_data_mart(self, humane_readable_name, comment, email, password):
        if email and password != "":
            try:
                user = user_data_access.get_by_email(email)

                if not user:
                    raise Exception("wrong credentials")

                if sha256.verify(password, user.password_hash):
                    dm = create_datamart(
                        user,
                        self.datamart.metadata.target,
                        self.datamart.metadata.target,
                        humane_readable_name,
                        comment
                    )

                    dm.metadata.heritage.append(self.datamart)
                    dm.save()

                    self.spark_helper.write_datamart(dm, self.dataframe)

                    return html.Div([
                        dbc.Alert(html.Div([
                            "Successfully stored the data mart: ",
                            dcc.Link(href="/dashboard/" + dm.uid)
                        ]), color="success"),
                    ])
                else:
                    raise Exception("wrong credentials")
            except Exception as e:
                return html.Div([
                    dbc.Alert(str(e), color="danger"),
                ])

    def run_sql(self, value):
        try:
            sqlRequest = value
            viewName = ""
            if "FROM" in sqlRequest:
                viewName = sqlRequest.partition("FROM")[-1].replace(";", "").replace(",",
                                                                                     "").strip()
            elif "From" in sqlRequest:
                viewName = sqlRequest.partition("From")[-1].replace(";", "").replace(",",
                                                                                     "").strip()
            elif "from" in sqlRequest:
                viewName = sqlRequest.partition("from")[-1].replace(";", "").replace(",",
                                                                                     "").strip()
            viewName = viewName.split(" ")[0]

            self.dataframe.createOrReplaceTempView(viewName)

            self.df_datamart = self.spark.sql(sqlRequest)
            self.df_datamart_pandas = self.df_datamart.toPandas()
            self.df_datamart
            return html.Div([
                DataTable(
                    id='datatable-paging-sql',
                    columns=[
                        {"name": i, "id": i} for i in sorted(self.df_datamart_pandas.columns)
                    ],
                    page_current=0,
                    page_size=self.PAGE_SIZE,
                    page_action='custom',
                    sort_action='custom',
                    sort_mode='single',
                    sort_by=[]
                ),
                dbc.Input(
                    id='input1DataMart',
                    type="text",
                    placeholder='human-readable name',
                    style={'width': '100%', 'margin-bottom': 10, 'margin-top': 10},
                ),
                dbc.Input(
                    id='input2DataMart',
                    type="text",
                    placeholder='comment',
                    style={'width': '100%', 'margin-bottom': 10},
                ),
                dbc.Input(
                    id='input3DataMart',
                    type="text",
                    placeholder='email',
                    style={'width': '100%', 'margin-bottom': 10},
                ),
                dbc.Input(
                    id='input4DataMart',
                    type="password",
                    placeholder='password',
                    style={'width': '100%', 'margin-bottom': 10},
                ),
                dbc.Button('Save Data Mart', id='input-dataMart-button', n_clicks=0),
                html.Div(id='dataMart-output',
                         style={'whiteSpace': 'pre-line', 'margin-top': 10, 'margin-bottom': 10}),
            ])
        except Exception as e:
            return html.Div([
                dbc.Alert(str(e), color="danger"),
            ])
