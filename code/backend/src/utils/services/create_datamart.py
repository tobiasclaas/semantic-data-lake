import uuid
from datetime import datetime

from werkzeug.exceptions import NotAcceptable

from database.models import User, Datamart, Metadata, MongodbStorage, PostgresqlStorage, CsvStorage, \
    XmlStorage, JsonStorage, DatamartStatus
from settings import Settings

settings = Settings()


def __get_target__(source, target_storage, workspace_id, uid):
    """
    Helper function to set model values
    
    :param source: source object
    :param target_storage: where to store the DataMart, possible values MongoDB, Postgres, HDFS
    :returns: corresponding Storage Object.
    """
    if target_storage == "MongoDB":
        return MongodbStorage(
            host=settings.mongodb_storage.host,
            port=settings.mongodb_storage.port,
            user=settings.mongodb_storage.user,
            password=settings.mongodb_storage.password,
            database=workspace_id,
            collection=uid
        )

    elif target_storage == "PostgreSQL":
        print(workspace_id)
        return PostgresqlStorage(
            host=settings.postgresql_storage.host,
            port=settings.postgresql_storage.port,
            user=settings.postgresql_storage.user,
            password=settings.postgresql_storage.password,
            database=f"workspace_"+workspace_id,
            table=uid
        )

    elif target_storage == "HDFS":
        folder = settings.hdfs_storage.storage_directory

        if source and isinstance(source, CsvStorage):
            return CsvStorage(
                file=f"{folder}/{workspace_id}/{uid}.csv",
                has_header=source.has_header,
                delimiter=source.delimiter
            )

        elif source and isinstance(source, XmlStorage):
            return XmlStorage(
                file=f"{folder}/{workspace_id}/{uid}.xml",
                row_tag=source.row_tag
            )

        else:
            return JsonStorage(
                file=f"{folder}/{workspace_id}/{uid}.json"
            )
    else:
        raise NotAcceptable(
            f"Unknown target storage {target_storage} (allowed: 'MongoDB', 'PostgreSQL', 'HDFS')"
        )


def create_datamart(user: User, source, target_storage, workspace_id, human_readable_name, comment):
    """
    Helper function to create DataMart entry with metadata

    :param user: user
    :param source: source object
    :param target_storage: where to store the DataMart, possible values MongoDB, Postgres, HDFS
    :param workspace_id: workspace_id for the datamart
    :param human_readable_name: name for the datamart
    :param comment: a comment for the DataMart
    :returns: Datamart Object.
    """
    uid = str(uuid.uuid4())
    datamart = Datamart(
        uid=uid,
        workspace_id=workspace_id,
        human_readable_name=human_readable_name,
        comment=comment,
        metadata=Metadata(
            created_at=datetime.now(),
            created_by=None,
            heritage=[],
            construction_code="",
            construction_query="",
            source=source,
            target=__get_target__(source, target_storage, workspace_id, uid)
        ),
        status=DatamartStatus()
    )

    datamart.save()

    return datamart
