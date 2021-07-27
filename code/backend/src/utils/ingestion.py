from datetime import datetime

from pyspark.sql import DataFrame, functions
from werkzeug.exceptions import NotAcceptable
from database.data_access import datamart_data_access as data_access

from utils.spark import SparkHelper
from database.models import (
    Datamart, MongodbStorage, PostgresqlStorage,
    CsvStorage, JsonStorage, XmlStorage, DatamartState
)
from settings import Settings

settings = Settings()


def ingest(datamart: Datamart):
    """
    Using the datamart.metadata.source and datamart.metadata.target fields, reads from source
    and writes Pyspark dataframe object to the given target using a Spark session. 
    :param datamart: Datamart object, containing all information from where to read and
    where to write.
    :return: Datamart object. The same datamart object is returned with few fields modified
    """
    spark_helper = None
    try:
        spark_helper = SparkHelper(f"ingest_{datamart.uid}")

        source = datamart.metadata.source
        target = datamart.metadata.target

        dataframe: DataFrame

        # read
        if isinstance(source, MongodbStorage):
            dataframe = spark_helper.read_mongodb(source)

        elif isinstance(source, PostgresqlStorage):
            dataframe = spark_helper.read_postrgesql(source)

        elif isinstance(source, CsvStorage):
            dataframe = spark_helper.read_csv(source)

        elif isinstance(source, JsonStorage):
            dataframe = spark_helper.read_json(source)

        elif isinstance(source, XmlStorage):
            dataframe = spark_helper.read_xml(source)

        else:
            raise NotAcceptable("invalid source storage")

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



def ingest_spark_helper(datamart: Datamart, spark_helper, dataframe):
    """
    Used in workflow api. Using the datamart.metadata.source 
    and datamart.metadata.target fields, reads from source and
    writes Pyspark dataframe object to the given target using a Spark session.
    :param datamart: Datamart object.
    :param spark_helper: SparkHelper object, that contains all configuration for the Cluster.
    :param dataframe: Dataframe (pyspark) object.
    :return: Datamart object.
    """
    try:
        source = datamart.metadata.source
        target = datamart.metadata.target

        dataframe: DataFrame

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

    marts = source.file.split(',')
    heritage = []
    for mart in marts:
        mart = data_access.get_by_uid(mart)
        heritage.append(mart)

    datamart.metadata.heritage = heritage
    datamart.metadata.schema = dataframe.schema.json()
    datamart.status.state = DatamartState.SUCCESS
    datamart.status.error = None
    datamart.status.ended = datetime.now()

    datamart.save()

    spark_helper.spark_session.stop()

    return datamart
