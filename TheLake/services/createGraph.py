from spark import SparkHelper
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
from pyspark.sql import *
from pyspark.sql.types import StructType 
from models.metaData import Ancestor, MetaData
from models.user import User
from models.job import Job
from datetime import datetime
import uuid
from apscheduler.schedulers.background import BackgroundScheduler
import os
import pyspark.sql.functions as F
import json

class Dashboard():
  PAGE_SIZE = 20
  dfPandas = None
  df = None
  mD = None
  spark = None
  dfDataMart = None
  dfDataMartPandas = None

  def dataAccess(self, id, app):
    self.mD = MetaData.objects(uid__exact = id).get()

    self.spark = SparkSession.builder.master(app.config['SPARK_MASTER'])\
        .appName(str(uuid.uuid4()))\
        .config('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector_2.12:3.0.0,org.postgresql:postgresql:42.2.18,com.databricks:spark-xml_2.12:0.10.0')\
        .getOrCreate()

    if self.mD.targetStorageSystem == "MongoDB":
        #authUrl = f"mongodb://{app.config['MONGO_USER']}:{app.config['MONGO_PASSWORD']}@{app.config['MONGO_HOST']}:{app.config['MONGO_PORT']}"
        authUrl = f"mongodb://{app.config['MONGO_HOST']}:{app.config['MONGO_PORT']}"
        df = self.spark.read.format("com.mongodb.spark.sql.DefaultSource")\
                .option("user", app.config['MONGO_USER']).option("password", app.config['MONGO_PASSWORD'])\
                .option("spark.mongodb.input.uri", authUrl) \
                .option("database", "dataLakeStorage").option("collection", self.mD.uid).load()

    elif self.mD.targetStorageSystem == "PostgreSQL":
        df = self.spark.read \
            .format("jdbc") \
            .option("url", self.mD.targetURL) \
            .option("dbtable", f'"{str(self.mD.uid)}"') \
            .option("user", app.config['POSTGRES_USER']) \
            .option("password", app.config['POSTGRES_PASSWORD']) \
            .option("driver", "org.postgresql.Driver") \
            .load()
    else:
        if self.mD.mimetype == "text/csv":
            df = self.spark.read \
                .format("csv") \
                .option("delimiter", self.mD.csvDelimiter) \
                .option('header', self.mD.csvHasHeader) \
                .option("inferSchema", True) \
                .load(self.mD.targetURL)
        elif self.mD.mimetype == "application/xml":
            df = self.spark.read \
            .format("com.databricks.spark.xml") \
            .option("rowTag", self.mD.xmlRowTag) \
            .load(self.mD.targetURL)
        else:
            df = self.spark.read \
            .option("multiline", False) \
            .json(self.mD.targetURL)
    self.dfPandas = df.toPandas()
    self.df = df
    '''if returnDf == False:
        returnList = [] 
        for row in df.toJSON().collect():
            returnList.append(json.loads(row)) 
        return jsonify({"data":returnList})'''

  def createGraph(self, pathname, app):
    self.mD = MetaData.objects(uid__exact = pathname).get()
    sparkHelper = SparkHelper("Dashboard")
    self.df = sparkHelper.readFromMetadata(self.mD)
    self.dfPandas = self.df.toPandas()
    '''self.dfPandas = self.dataAccess(pathname, app)
    self.dfPandas = self.df.toPandas()'''

    return html.Div(children=[
                      html.Div(className='row',
                              style={'padding': 10},
                              id=pathname,
                              children=[
                                    dbc.Col(html.Div(children=[
                                      html.H1(pathname),
                                      html.H2("Data"),
                                      DataTable(
                                        id='datatable-paging',
                                        columns=[
                                            {"name": i, "id": i} for i in sorted(self.dfPandas.columns)
                                        ],
                                        page_current=0,
                                        page_size=self.PAGE_SIZE,
                                        page_action='custom',
                                        sort_action='custom',
                                        sort_mode='single',
                                        sort_by=[]
                                      ),
                                    ]),width=12),
                                    dbc.Col(html.Div(children=[
                                    html.H2("SQL"),
                                    dbc.Textarea(
                                      id='textarea-sql',
                                      placeholder='SELECT * FROM ViewName;',
                                      value='SELECT * FROM ViewName;',
                                      style={'width': '100%', 'height': 200, 'margin-bottom':10},
                                    ),
                                    dbc.Button('Submit', id='textarea-sql-button', n_clicks=0),
                                    html.Div(id='textarea-sql-output', style={'whiteSpace': 'pre-line', 'margin-top':10,'margin-bottom':10}),
                                    ]),width=12),
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
                                      style={'width': '100%', 'height': 200, 'margin-bottom':10},
                                    ),
                                    dbc.Button('Submit', id='textarea-graph-button', n_clicks=0),
                                    html.Div(id='textarea-graph-output', style={'whiteSpace': 'pre-line', 'margin-top':10, 'margin-bottom':10}),
                                    ]),width=12),
                                  ])
                                ])

  def tablePaging(self, page_current, page_size, sort_by):
    if len(sort_by):
        dff = self.dfPandas.sort_values(
            sort_by[0]['column_id'],
            ascending=sort_by[0]['direction'] == 'asc',
            inplace=False
        )
    else:
        dff = self.dfPandas
    return dff.iloc[
          page_current*page_size:(page_current+ 1)*page_size
      ].to_dict('records')
  
  def tablePagingSQL(self, page_current, page_size, sort_by):
    if len(sort_by):
      dff = self.dfDataMartPandas.sort_values(
          sort_by[0]['column_id'],
          ascending=sort_by[0]['direction'] == 'asc',
          inplace=False
      )
    else:
        dff = self.dfDataMartPandas
    return dff.iloc[
          page_current*page_size:(page_current+ 1)*page_size
      ].to_dict('records')
  

  def addTable(self, value):
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
  
  def saveDataMart(self, humanReadableName, comment, email, password):
    if email and password != "": 
      try: 
        currentUser = User.objects(email__exact=email).get()
        if not currentUser:
          raise Exception("wrong credentials")

        if User().verifyHash(password, currentUser.password):
          heritage = []
          metadata: MetaData = self.mD
          ancestor = Ancestor(
            uid=str(metadata.uid),
            hrn=metadata.humanReadableName,
            heritage=metadata.heritage
          )
          heritage.append(ancestor)

          apiUser = currentUser
          uid = str(uuid.uuid4())
          sparkHelper = SparkHelper("Dashboard")
          if metadata.targetStorageSystem == "MongoDB":
            targetURL = sparkHelper.writeMongodb(self.dfDataMart, uid)
            #targetURL = ""
          elif metadata.targetStorageSystem == "PostgreSQL":
            targetURL = sparkHelper.writePostgres(self.dfDataMart, uid)
          else:
            if metadata.mimetype == 'CSV':
              mimetype = "text/csv"
              filename = uid + ".csv"
              targetURL = sparkHelper.writeCSV(self.dfDataMart, filename, metadata.csvDelimiter, metadata.csvHasHeader)
            elif metadata.mimetype == 'XML':
              mimetype = "application/xml"
              filename = uid + ".xml"
              targetURL = sparkHelper.writeXML(self.dfDataMart, filename, metadata.xmlRowTag)
            elif metadata.mimetype == 'JSON':
              mimetype = "application/json"
              filename = uid + ".json"
              targetURL = sparkHelper.writeJSON(self.dfDataMart, filename)


          metadata = MetaData(
            uid=uid,
            isDatabase=True,
            schema=self.dfDataMart.schema.json(),
            insertedAt=datetime.now(),
            insertedBy=apiUser,
            targetStorageSystem="MongoDB",
            targetURL=targetURL,
            heritage=heritage,
            humanReadableName=humanReadableName,
            comment=comment
          )
          metadata.save()
          return html.Div([
            dbc.Alert(html.Div([
              "Successfully stored the data mart: ",
              dcc.Link(href="/dashboard/"+uid)
            ]) , color="success"),
          ])
        else:
          raise Exception("wrong credentials")
      except Exception as e:
        return html.Div([
          dbc.Alert(str(e), color="danger"),
        ])

  def runSQL(self, value):
    try:
      sqlRequest = value
      viewName = ""
      if "FROM" in sqlRequest:
        viewName = sqlRequest.partition("FROM")[-1].replace(";", "").replace(",", "").strip()
      elif "From" in sqlRequest:
        viewName = sqlRequest.partition("From")[-1].replace(";", "").replace(",", "").strip()
      elif "from" in sqlRequest:
        viewName = sqlRequest.partition("from")[-1].replace(";", "").replace(",", "").strip() 
      viewName = viewName.split(" ")[0]

      self.df.createOrReplaceTempView(viewName)

      self.dfDataMart = self.spark.sql(sqlRequest)
      self.dfDataMartPandas = self.dfDataMart.toPandas()
      self.dfDataMart
      return html.Div([
        DataTable(
          id='datatable-paging-sql',
          columns=[
              {"name": i, "id": i} for i in sorted(self.dfDataMartPandas.columns)
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
          style={'width': '100%', 'margin-bottom':10, 'margin-top':10},
        ),
        dbc.Input(
          id='input2DataMart',
          type="text",
          placeholder='comment',
          style={'width': '100%', 'margin-bottom':10},
        ),
        dbc.Input(
          id='input3DataMart',
          type="text",
          placeholder='email',
          style={'width': '100%', 'margin-bottom':10},
        ),
        dbc.Input(
          id='input4DataMart',
          type="password",
          placeholder='password',
          style={'width': '100%', 'margin-bottom':10},
        ),
        dbc.Button('Save Data Mart', id='input-dataMart-button', n_clicks=0),
        html.Div(id='dataMart-output', style={'whiteSpace': 'pre-line', 'margin-top':10,'margin-bottom':10}),
      ])
    except Exception as e:
        return html.Div([
          dbc.Alert(str(e), color="danger"),
        ])