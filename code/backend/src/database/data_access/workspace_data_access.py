import os

from database.models import Workspace
from werkzeug.exceptions import NotFound, BadRequest
from requests import put, post, delete as delete_request
from database.data_access import ontology_data_access
from werkzeug.datastructures import FileStorage


def get_all() -> [Workspace]:
    return Workspace.objects.all()


def create(name):
    entity = Workspace(name=name)
    Workspace.objects.insert(entity)
    # create dataset in fuseki
    post('http://localhost:3030/$/datasets', auth=('admin', 'pw123'),
         data={'dbName': str(entity.id), 'dbType': 'tdb'})
    # upload poa ontology
    __location__ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    file_location = os.path.join(__location__, "Resources", "propertyorattribute.n3")
    with open(file_location, 'rb') as fp:
        file = FileStorage(fp)
        ontology_data_access.add("Property or Attribute", file, entity.id)
    return entity


def delete(id):
    entity: Workspace = Workspace.objects(id__exact=id)
    if not entity:
        raise NotFound()
    if len(get_all()) == 1:
        raise BadRequest()
    delete_request('http://localhost:3030/$/datasets/{}'.format(id), auth=('admin', 'pw123'))
    Workspace.objects(id__exact=id).delete()
