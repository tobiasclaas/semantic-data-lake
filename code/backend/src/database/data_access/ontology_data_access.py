import os
from requests import post, delete as delete_request

import settings
from database.models import Ontology
from werkzeug.exceptions import NotFound, BadRequest
from database.models.workspace import Workspace


def get_all(workspace_id) -> [Ontology]:
    """
    Get all ontologies in a specific workspace.

    :param workspace_id: id of workspace.
    :returns: all ontologies in the workspace.
    """
    workspace = Workspace.objects(id__exact=workspace_id).get()
    return Ontology.objects(workspace=workspace).all()


def add(name, file, workspace_id) -> Ontology:
    """
    Adds new ontology to Fuseki and adds an entry in MongoDB.

    :param name: name of the ontology.
    :param file: file that contains the ontology.
    :param workspace_id: the workspace the file is to be added in Fuseki.
    :returns: the newly created Ontology entity in MongoDB.
    """
    workspace = Workspace.objects(id__exact=workspace_id).get()
    if not workspace:
        raise BadRequest()

    entity = Ontology(
        name=name,
        workspace=workspace)
    Ontology.objects.insert(entity)

    file_extension = os.path.splitext(file.filename)[1].lower()

    if ".n3" == file_extension:
        headers = {'Content-Type': 'text/n3; charset=utf-8'}
    elif ".rdf" == file_extension:
        headers = {'Content-Type': 'application/rdf+xml; charset=utf-8'}
    elif ".owl" == file_extension:
        headers = {'Content-Type': 'application/rdf+xml; charset=utf-8'}
    elif ".jsonld" == file_extension:
        headers = {'Content-Type': 'application/ld+json; charset=utf-8'}
    else:
        raise TypeError(file_extension.lower() + " is not supported")

    post('http://localhost:3030/{}?graph={}'.format(workspace_id, str(entity.id)), data=file, headers=headers)
    return entity


def delete(workspace_id, graph_id):
    """
    Delete ontology in Fuseki and the entry in MongoDB.

    :param workspace_id: id of workspace in MongoDB and Fuseki.
    :param graph_id: name of named graph.
    :return:
    """
    entity: Ontology = Ontology.objects(id__exact=graph_id)
    if not entity:
        raise NotFound()
    entity = entity.get()
    if str(entity.workspace.id) != workspace_id:
        raise NotFound()
    delete_request('http://localhost:3030/{}?graph={}'.format(workspace_id, graph_id))
    entity.delete()


def create_query_string(graph_name: str, keyword: str):
    """
    This methods generates the query string for the keyword-search in put.

    :param graph_name: graph to be queried, default is "default graph",
        like "<http://localhost:3030/60d5c79a7d2c38ee678e87a8/60d5c79d7d2c38ee678e87a9>"
    :param keyword: keywords to search for or when search-bool is false the query itself
    :returns: the query
    """
    if graph_name == '' or graph_name is None:
        graph_name = '?g'
    query = """ SELECT ?subject ?predicate ?object
                WHERE {
                    GRAPH """ + graph_name + """ {
                        ?subject ?predicate ?object .
                        FILTER (
                            regex(str(?subject), '""" + keyword + """') ||
                            regex(str(?predicate), '""" + keyword + """') ||
                            regex(str(?object),  '""" + keyword + """'))
                    }
                } """
    return query


def get_suggestions(workspace_id, search_term):
    """
    This function provides multiple suggestions for a auto-completion of ontology-attributes in fuseki. The search_term
        can either be the rdf:label or the name of the class itself(after the #).

    :returns: a list of maximum 20 suggestions which fit the requirements ordered by the length of the label.
    """
    querystring = """
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX ncit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
        SELECT ?subject ?label ?desc
        WHERE {
          ?subject a ?x ;
            rdfs:label ?label .
          OPTIONAL {?subject ncit:P97 ?desc .}
          FILTER (regex(str(?subject), '#""" + search_term + """', 'i') || 
            regex(?label, '""" + search_term + """', 'i'))
        }
        ORDER BY strlen(?label)
        LIMIT 20 """
    p = post('http://localhost:3030/' + workspace_id,
             auth=(settings.Settings().fuseki_storage.user, settings.Settings().fuseki_storage.password),
             data={'query': querystring})

    return p.content


def add_standard_ontology(entity):
    post('http://localhost:3030/$/datasets',
         auth=(settings.Settings().fuseki_storage.user, settings.Settings().fuseki_storage.password),
         data={'dbName': str(entity.id), 'dbType': 'tdb'})
