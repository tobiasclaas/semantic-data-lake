import os

import psycopg2
from database.models import Workspace, Ontology
from werkzeug.exceptions import NotFound, BadRequest
from requests import put, post, delete as delete_request
from database.data_access import ontology_data_access
from werkzeug.datastructures import FileStorage
from settings import Settings
import mongoengine
from pywebhdfs.webhdfs import PyWebHdfsClient




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
    if len(get_all()) == 1:
        raise BadRequest()
    entity: Workspace = Workspace.objects(id__exact=workspace_id)
    if len(entity) == 0:
        raise NotFound()
    entity = entity.get()
    if entity.name == 'Default Workspace':
        return None
    # delete workspace in fuseki
    delete_request('http://localhost:3030/$/datasets/{}'.format(workspace_id), auth=('admin', 'pw123'))
    # delete workspace folder in hdfs
    settings = Settings()
    client = PyWebHdfsClient(host=settings.hdfs_storage.namenode, port="9870")
    client.delete_file_dir("/datalake_storage/" + workspace_id, recursive=True)
    # delete database in MongoDB based on workspace_id
    # drop database here
    # delete database in postgres based on workspace_id
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
        cur.execute("DROP DATABASE workspace_" + workspace_id + ";")
        connection.close()
    # delete ontology entries in MongoDB
    Ontology.objects(workspace=workspace_id).delete()
    Workspace.objects(id__exact=workspace_id).delete()
