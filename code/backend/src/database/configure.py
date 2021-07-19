import psycopg2
from passlib.hash import pbkdf2_sha256 as sha256
from werkzeug.exceptions import NotFound

from settings import Settings
from database import FlaskDocument
from database.data_access import user_data_access, workspace_data_access, annotation_data_access
from database.models import User


def initialize():
    settings = Settings()

    # ===== create user if not exists ==============================================================
    try:
        user_data_access.get_by_email("admin")
    except NotFound:
        user = User(
            email="admin",
            password_hash=sha256.hash("admin"),
            firstname="Admin",
            lastname="User",
            is_admin=True
        )
        user.save()

    # ===== init postgresql ========================================================================
#    postgresql = settings.postgresql_storage
#    for item in workspace_data_access.get_all():
#        if item.name == "Default Workspace":
#            default_workspace_id = f"workspace_" + f"{item.id}"
#    connection = None

#    try:
#        connection = psycopg2.connect(
#            f"host='{postgresql.host}' user='{postgresql.user}' password='{postgresql.password}'" +
#            f" port='{postgresql.port}'"
#        )
#    except psycopg2.OperationalError as err:
#        print(f"[POSTGRES] error while creating:\n\t{err}")
#
#    if connection is not None and default_workspace_id is not None:
#        connection.autocommit = True
#        cur = connection.cursor()
#        cur.execute("SELECT datname FROM pg_database;")
#        list_database = cur.fetchall()
#        # print(list_database)
#        #  and (postgresql.database,) != (None,)
#        if (default_workspace_id,) not in list_database:
#            cur.execute(f"CREATE DATABASE " + default_workspace_id)
#            print(f"[POSTGRES] created storage database")
#        connection.close()


def drop_collections():
    for klass in FlaskDocument.all_subclasses():
        klass.drop_collection()
