from apscheduler.schedulers.background import BackgroundScheduler
from mongoengine.fields import StringField
from pywebhdfs.webhdfs import PyWebHdfsClient
from business_logic.spark import SparkHelper
from database.models import Dataset 
from werkzeug.exceptions import NotFound, BadRequest

from database.models.workspace import Workspace
from requests import put, post, delete as DeleteRequest
import os

from settings import Settings

def get_all(workspace_id) -> [Dataset]:
    workspace = Workspace.objects(id__exact=workspace_id).get()
    return Dataset.objects(workspace=workspace).all()

def add_csv(name, file, delimiter, has_header, workspace_id) -> Dataset:
    workspace = Workspace.objects(id__exact=workspace_id).get()
    if not workspace:
        raise BadRequest()

    entity = Dataset(
        name=name,
        type="csv",
        workspace = workspace
    )
    Dataset.objects.insert(entity)
    hdfs = Settings.Settings().hdfs_storage
    client = PyWebHdfsClient(host=hdfs.namenode, port="9870")
    client.create_file(f"{hdfs.ingestion_directory}/{str(entity.id)}", file)

    try:
        scheduler = BackgroundScheduler()

        scheduler.add_job(
            lambda: ingest(entity)
        )

        scheduler.start()
    except Exception as e:
        return e
    
    return entity


def ingest(dataset: Dataset):
    spark_helper = None
    try:
        spark_helper = SparkHelper(f"ingest_{str(dataset.id)}")

        source = datamart.metadata.source
        target = datamart.metadata.target

        dataframe: DataFrame

      
      
        dataframe = spark_helper.read_csv(source)


    
        # write
        if isinstance(target, MongodbStorage):
            spark_helper.write_mongodb(dataframe, target)

        elif isinstance(target, PostgresqlStorage):
            if isinstance(source, CsvStorage) or isinstance(source, JsonStorage) or isinstance(source, XmlStorage):
                raise NotAcceptable(f"Cannot save file in prostgres")

            elif isinstance(source, MongodbStorage):
                flat_cols = [c[0] for c in dataframe.dtypes if c[1][:6] != 'struct']
                nested_cols = [c[0] for c in dataframe.dtypes if c[1][:6] == 'struct']
                flattened_dataframe = dataframe.select(
                    flat_cols + [
                        functions.col(nc + '.' + c).alias(nc + '_' + c)
                        for nc in nested_cols
                        for c in dataframe.select(nc + '.*').columns
                    ]
                )
                dataframe = flattened_dataframe

            spark_helper.write_postgresql(dataframe, target)

        elif isinstance(target, CsvStorage):
            spark_helper.write_csv(dataframe, target)

        elif isinstance(target, JsonStorage):
            spark_helper.write_json(dataframe, target)

        elif isinstance(target, XmlStorage):
            spark_helper.write_xml(dataframe, target)

        else:
            raise NotAcceptable("invalid target storage")

    except Exception as e:
        if spark_helper:
            spark_helper.spark_session.stop()

        datamart.status.state = DatamartState.FAILED
        datamart.status.error = f"{e}"
        datamart.status.ended = datetime.now()
        datamart.save()
        return datamart

    dataframe.show()
    print(dataframe.schema)

    datamart.metadata.schema = dataframe.schema.json()
    datamart.status.state = DatamartState.SUCCESS
    datamart.status.error = None
    datamart.status.ended = datetime.now()

    datamart.save()

    spark_helper.spark_session.stop()

    return datamart
