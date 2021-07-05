import os

from database.models import Workspace
from werkzeug.exceptions import NotFound, BadRequest
from requests import put, post, delete as delete_request
from database.data_access import ontology_data_access
from werkzeug.datastructures import FileStorage
import psycopg2
from settings import Settings


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

    # create database in postgres based on workspace_id
    settings = Settings()
    postgresql = settings.postgresql_storage
    connection = None
    try:
        connection = psycopg2.connect(
            f"host='{postgresql.host}' user='{postgresql.user}' password='{postgresql.password}'" +
            f" port='{postgresql.port}'"
        )
    except psycopg2.OperationalError as err:
        print(f"[POSTGRES] error while creating:\n\t{err}")

    if connection is not None:
        connection.autocommit = True
        cur = connection.cursor()
        cur.execute("SELECT datname FROM pg_database;")
        list_database = cur.fetchall()
        if (entity.id,) not in list_database:
            cur.execute(f"CREATE DATABASE " + "workspace_" + str(entity.id))
            print(f"[POSTGRES] created storage database")
        connection.close()

    return entity


def delete(workspace_id):
    entity: Workspace = Workspace.objects(id__exact=workspace_id)
    if entity.name == 'Default Workspace':
        return None
    if not entity:
        raise NotFound()
    if len(get_all()) == 1:
        raise BadRequest()
    delete_request('http://localhost:3030/$/datasets/{}'.format(workspace_id), auth=('admin', 'pw123'))
    Workspace.objects(id__exact=workspace_id).delete()
