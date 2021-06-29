import os

from database.models import Ontology
from werkzeug.exceptions import NotFound, BadRequest

from database.models.workspace import Workspace
from requests import put, post, delete as delete_request


def get_all(workspace_id) -> [Ontology]:
    workspace = Workspace.objects(id__exact=workspace_id).get()
    return Ontology.objects(workspace=workspace).all()


def add(name, file, workspace_id) -> Ontology:
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


def delete(graph_id, workspace_id):
    entity: Ontology = Ontology.objects(id__exact=graph_id)
    if not entity:
        raise NotFound()
    entity = entity.get()
    if str(entity.workspace.id) != workspace_id:
        raise NotFound()
    delete_request('http://localhost:3030/{}?graph={}'.format(workspace_id, graph_id))
    entity.delete()
