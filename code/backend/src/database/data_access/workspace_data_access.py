import os
import psycopg2
import pymongo
from pywebhdfs.webhdfs import PyWebHdfsClient
from requests import post, delete as delete_request
from werkzeug.exceptions import NotFound, BadRequest
from werkzeug.datastructures import FileStorage

from database.models import Workspace, Ontology
from database.data_access import ontology_data_access
from settings import Settings


def get_all(user) -> [Workspace]:
    """
    Get all workspaces for a specific user.

    :param user: user.
    :returns: all workspace for a specific user.
    """
    workspaces = Workspace.objects(user=user).all()
    if len(workspaces) == 0:
        create("Default Workspace", user)
        workspaces = Workspace.objects(user=user).all()

    return workspaces


def create(name, user):
    """
    Create a new workspaces for a specific user. This will create a new postgres database
    and add a the standard ontology. 

    :param user: user.
    :param name: name of the new workspace.
    :returns: Workspace object.
    """
    entity = Workspace(name=name, user=user)
    Workspace.objects.insert(entity)
    settings = Settings()

    # create dataset in fuseki
    ontology_data_access.create_workspace_fuseki(entity)

    # get path of resource folder
    __location__ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.realpath(__file__)))))))
    file_location = os.path.join(__location__, "resources", "propertyorattribute.n3")

    with open(file_location, 'rb') as fp:
        file = FileStorage(fp)
        ontology_data_access.add("Property or Attribute", file, entity.id)

    # create database in postgres based on workspace_id
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


def delete(workspace_id, user):
    """
    Delete a given workspaces for a specific user. This will delete the associated 
    Postgres Fuseki MongoDB databases and the HDFS folder as well as the metadata entries
    in MongoDB.

    :param workspace_id: id of the workspace.
    :param user: user.
    :returns: Workspace object.
    """
    if len(get_all(user)) == 1:
        raise BadRequest()

    entity: Workspace = Workspace.objects(id__exact=workspace_id, user=user)
    if len(entity) == 0:
        raise NotFound()

    # delete workspace in fuseki
    delete_request('http://localhost:3030/$/datasets/{}'.format(workspace_id),
                   auth=(Settings().fuseki_storage.user, Settings().fuseki_storage.password))

    # delete workspace folder in hdfs based on workspace_id
    settings = Settings()
    client = PyWebHdfsClient(host=settings.hdfs_storage.namenode, port="9870")
    client.delete_file_dir("/datalake_storage/" + workspace_id, recursive=True)
    client.delete_file_dir("/datalake_ingestion/" + workspace_id, recursive=True)

    # delete database in MongoDB based on workspace_id
    # auth = f"{storage.user}:{storage.password}@"
    uri = f"mongodb://{settings.mongodb_storage.user}:{settings.mongodb_storage.password}@{settings.mongodb_storage.host}:{settings.mongodb_storage.port}/?authSource=admin"
    mongo_client = pymongo.MongoClient(uri)
    mongo_client.drop_database(workspace_id)

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
