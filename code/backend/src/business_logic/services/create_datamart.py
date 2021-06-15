import uuid
from datetime import datetime

from werkzeug.exceptions import NotAcceptable

from database.models import User, Datamart, Metadata, MongodbStorage, PostgresqlStorage, CsvStorage, \
    XmlStorage, JsonStorage, DatamartStatus
from settings import Settings

settings = Settings()


def __get_target__(source, target_storage, workspace, uid):
    if target_storage == "MongoDB":
        return MongodbStorage(
            host=settings.mongodb_storage.host,
            port=settings.mongodb_storage.port,
            user=settings.mongodb_storage.user,
            password=settings.mongodb_storage.password,
            database=settings.mongodb_storage.database,
            collection=uid
        )

    elif target_storage == "PostgreSQL":
        return PostgresqlStorage(
            host=settings.postgresql_storage.host,
            port=settings.postgresql_storage.port,
            user=settings.postgresql_storage.user,
            password=settings.postgresql_storage.password,
            database=settings.postgresql_storage.database,
            table=uid
        )

    elif target_storage == "HDFS":
        folder = settings.hdfs_storage.storage_directory

        if source and isinstance(source, CsvStorage):
            return CsvStorage(
                file=f"{folder}/{workspace}/{uid}.csv",
                has_header=source.has_header,
                delimiter=source.delimiter
            )

        elif source and isinstance(source, XmlStorage):
            return XmlStorage(
                file=f"{folder}/{workspace}/{uid}.xml",
                row_tag=source.row_tag
            )

        else:
            return JsonStorage(
                file=f"{folder}/{workspace}/{uid}.json"
            )
    else:
        raise NotAcceptable(
            f"Unknown target storage {target_storage} (allowed: 'MongoDB', 'PostgreSQL', 'HDFS')"
        )


def create_datamart(user: User, source, target_storage, workspace, human_readable_name, comment, uid):
    datamart = Datamart(
        uid=uid,
        human_readable_name=human_readable_name,
        comment=comment,
        metadata=Metadata(
            created_at=datetime.now(),
            created_by=user,
            heritage=[],
            construction_code="",
            construction_query="",
            source=source,
            target=__get_target__(source, target_storage, workspace, uid)
        ),
        status=DatamartStatus()
    )

    datamart.save()

    return datamart
