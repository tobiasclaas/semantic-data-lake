import json
from flask_restful import Resource
from flask_restful.reqparse import Argument
from requests import put, post, delete as delete_request

from api.services.decorators import parse_params


def get_suggestions(workspace_id, search_term):
    """
    This function provides multiple suggestions for a auto-completion of ontology-attributes in fuseki
    :word: search string
    :return:
    """
    querystring = """
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?subject ?label
        WHERE {
          ?subject a ?x ;
            rdfs:label ?label .
          FILTER (regex(str(?subject), '""" + search_term + """', 'i') || 
            regex(?label, '""" + search_term + """', 'i'))
        }
        ORDER BY strlen(?label)
        LIMIT 10    """
    p = post('http://localhost:3030/' + workspace_id, auth=('admin', 'pw123'), data={'query': querystring})

    try:
        data = json.loads(p.content)
        return data
    except Exception:
        return p.status_code


class Completion(Resource):
    @parse_params(
        Argument('workspace_id', required=True, type=str),
        Argument('search_term', required=True, type=str)
    )
    def get(self, workspace_id, search_term=''):
        return get_suggestions(workspace_id, search_term)
