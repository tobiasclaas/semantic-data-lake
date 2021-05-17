from flask import jsonify
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from flask_restful.reqparse import Argument
from api.services.decorators import parse_params

from business_logic.services.mapper import mapper
from database.data_access import user_data_access
from database.models import User

from requests import put, get, post
import json
import pandas as pd
import os

class FusekiQuery(Resource):
    @jwt_required
    @parse_params(
        Argument("query", type=str),
        Argument("database", type=str)
    )

    def get(querystring: str, database: str):
        p = post('http://localhost:3030/'+database, auth=('admin', 'pw123'), data={'query':querystring}) 
        data = json.loads(p.content)
        
        if p.ok:
            print("Query sent successfully!")
            
        else:
            print("Something went wrong!")
        try:
            df = pd.json_normalize(data, ['results', 'bindings'])
            #df = df[["s.value", "p.value", "o.value"]]
            return {"query_result": df}
        except:
            #df = pd.json_normalize(data)
            print(p.text)

class FusekiCreateDatabase(Resource):
    @parse_params(
        Argument("databasename", type=str)
    )          

    def post(databasename: str):
        p = post('http://localhost:3030/$/datasets', auth=('admin', 'pw123'), data={'dbName': databasename, 'dbType': 'tdb'}) 
        if p.ok:
            return print(databasename, "created")
        else:            
            print("Something went wrong!")
        print(p.text)

class FusekiIngestion(Resource):
    @parse_params(
        Argument("query", type=str)
        #Argument("database", type=str)
        #Argument("file", type=FileStorage, location='files', required=True)
    )
    
    def put(file, databasename: str):

        data = open(file).read()
        import os.path
        extension = os.path.splitext(file)[1]
        if "n3" in extension.lower():
            headers = {'Content-Type': 'text/n3; charset=utf-8'}
            os.system('curl -X POST -H "Authorization: Basic $(echo -n admin:pw123 | base64)" -d @{} localhost:3030/{}'.format(file,databasename))
        
        elif "rdf" in extension.lower():
            headers = {'Content-Type': 'application/rdf+xml; charset=utf-8'}
            p = post('http://localhost:3030/{}/data?default'.format(databasename), data=data, headers=headers)
            if p.ok and "n3" not in extension.lower():
                return print( "file uploaded to", databasename)
            else:            
                print("Something went wrong!")
            print(p.text)
        
        elif "owl" in extension.lower():
            headers = {'Content-Type': 'application/rdf+xml; charset=utf-8'}
            p = post('http://localhost:3030/{}/data?default'.format(databasename), data=data, headers=headers)
            if p.ok and "n3" not in extension.lower():
                return print( "file uploaded to", databasename)
            else:            
                print("Something went wrong!")
            print(p.text)
        elif "jsonld" in extension.lower():
            headers = {'Content-Type': 'application/ld+json; charset=utf-8'}
            p = post('http://localhost:3030/{}/data?default'.format(databasename), data=data, headers=headers)  
        ### other formats need to be tested
        #elif "nt" in extension.lower():
        #    headers = {'Content-Type': 'text/plain; charset=utf-8'}
        #elif "nq" in extension.lower():
        #    headers = {'Content-Type': 'application/n-quads; charset=utf-8'}
        #    p = post('http://localhost:3030/{}/data?default'.format(databasename), data=data, headers=headers)
        #elif "trig" in extension.lower():
        #    headers = {'Content-Type': 'application/trig; charset=utf-8'}
        #    p = post('http://localhost:3030/{}/data?default'.format(databasename), data=data, headers=headers)
        else:
            print("Unsupported format! Supported formats are n3,rdf, owl, jsonld")



