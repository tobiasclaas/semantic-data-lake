from database.models import Workspace 
from werkzeug.exceptions import NotFound, BadRequest

def get_all() -> [Workspace]:
    return Workspace.objects.all()
    
def create(name):
    entity = Workspace(
        name=name
    )
    Workspace.objects.insert(entity)
    return entity

def delete(id):
    entity:Workspace = Workspace.objects(id__exact=id)
    if not entity:
        raise NotFound()
    if len(get_all()) == 1:
        raise BadRequest()
    Workspace.objects(id__exact=id).delete()
