from database.models import Workspace 
from werkzeug.exceptions import NotFound, BadRequest
from requests import put, post, delete as DeleteRequest

def get_all() -> [Workspace]:
    return Workspace.objects.all()
    
def create(name):
    entity = Workspace(
        name=name
    )
    Workspace.objects.insert(entity)
    post('http://localhost:3030/$/datasets', auth=('admin', 'pw123'), data={'dbName': str(entity.id) , 'dbType': 'tdb'})
    return entity

def delete(id):
    entity:Workspace = Workspace.objects(id__exact=id)
    if not entity:
        raise NotFound()
    if len(get_all()) == 1:
        raise BadRequest()
    DeleteRequest('http://localhost:3030/$/datasets/{}'.format(id), auth=('admin', 'pw123'))
    Workspace.objects(id__exact=id).delete()
