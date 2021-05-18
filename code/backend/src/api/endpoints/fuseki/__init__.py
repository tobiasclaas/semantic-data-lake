from flask_restful import Resource
from flask_restful.reqparse import Argument
from flask import request
from api.services.decorators import parse_params
from werkzeug.datastructures import FileStorage
from requests import put, post
import json
import pandas as pd
import os
import traceback

class Fuseki(Resource):
    @parse_params(
        Argument("databasename", type=str),
        )
    
    def post(self, databasename: str):
        """
        This method sends a request to the fuseki flask and creates a new workspace if no error occurs.
        :param databasename: is a string and name of the to be created workspace
        :returns whether the creation of a new workspace succeeded or not in bool value
        """
        
        if databasename:
            p = post('http://localhost:3030/$/datasets', auth=('admin', 'pw123'),
                 data={'dbName': databasename, 'dbType': 'tdb'})
        else:
            print("No databasename given")
        
        if p.ok:
            return p.ok
        else:
            return p.text


    @parse_params(
        Argument("databasename", type=str),
        Argument("querystring", type=str), 
        Argument("search", type=bool)
        )
    def get(self, databasename: str, querystring: str, search: bool):

        partone = 'SELECT ?s ?p ?o WHERE {{?s ?p ?o . FILTER (contains(?s, "%s") )}' % querystring
        parttwo = ' UNION {?s ?p ?o . FILTER (contains(?p, "%s") )}' % querystring
        partthree = ' UNION {?s ?p ?o . FILTER (contains(?o, "%s") )}}' % querystring
        string = partone+parttwo+partthree 
        """
        This method queries fuseki for terms associated with the query string. If the parameter search is given,
        this method queries fuseki for any triple containing the query string.
        :param querystring: keywords to search for
        :param database: name of the database
        :param search: bool whether to return all triples containing a given string 
        :return: #TODO, what is returned?
        # TODO, Are the "databases" databases or workspaces?
        """
        if search:   
            p = post('http://localhost:3030/'+ databasename, auth=('admin', 'pw123'), data={'query': string}) # replace admin and pw by environment variable defined in docker-compose.yaml
            print(databasename, querystring, search )
            data = json.loads(p.content)
            
            return data['results']['bindings']
#
            #if not p.ok:
            #    return None
#
            #try:
            #    return pd.json_normalize(data, ['results', 'bindings']) # @Tobias: Dieser Teil schmeißt mir Error: Dataframe Object not JSON Serializable. Würde gerne einen PD-Dataframe ausgeben. 
            #except Exception as ex:
            #    traceback.print_exception(type(ex), ex, ex.__traceback__)
        else:
            print("query")
            p = post('http://localhost:3030/' + databasename, auth=('admin', 'pw123'), data={'query': querystring})
            data = json.loads(p.content)
          
            return data['results']['bindings']
            #if not p.ok:
            #    return None
#
            #try:
            #    return pd.json_normalize(data, ['results', 'bindings']) # @Tobias: Dieser Teil schmeißt mir Error: Dataframe Object not JSON Serializable. Würde gerne einen PD-Dataframe ausgeben.
            #except Exception as ex:
            #    traceback.print_exception(type(ex), ex, ex.__traceback__)

    @parse_params(
        Argument("databasename", type=str),
        Argument("file", type=FileStorage, location='files'),
        Argument("overwrite", type=bool)
    )
    def put(self, file: FileStorage, databasename: str, overwrite: bool):
        """
        Upload a given file to a specified database.
        :param file: A file to be uploaded
        :param databasename: The name of the database
        :param overwrite: If parameter is passed, the existing triples will be deleted and replaced with incoming file
        :return: Boolean if post was successful or not
        """
        data = file
        #print(data)
        
        extension = os.path.splitext(file.filename)[1].lower()

        # other formats need to be tested
        if ".n3" == extension:
            headers = {'Content-Type': 'text/n3; charset=utf-8'}
        elif ".rdf" == extension:
            headers = {'Content-Type': 'application/rdf+xml; charset=utf-8'}
        elif ".owl" == extension:
            headers = {'Content-Type': 'application/rdf+xml; charset=utf-8'}
        elif ".jsonld" == extension:
            headers = {'Content-Type': 'application/ld+json; charset=utf-8'}
        # elif "nt" in extension.lower():
        #    headers = {'Content-Type': 'text/plain; charset=utf-8'}
        # elif "nq" in extension.lower():
        #    headers = {'Content-Type': 'application/n-quads; charset=utf-8'}
        # elif "trig" in extension.lower():
        #    headers = {'Content-Type': 'application/trig; charset=utf-8'}
        else:
            raise TypeError(extension.lower() + " is not supported")

        if not overwrite:
            p = post('http://localhost:3030/{}/data?default'.format(databasename), data=data, headers=headers)
        else:
            p = put('http://localhost:3030/{}/data?default'.format(databasename), data=data, headers=headers)

        return p.ok
