import json

from http import HTTPStatus

from database.models import *


class UnknownModel(Exception):
    """
    Class to display unknown model message.
    """

    def __init__(self, message, model=None):
        """
        Function to display unknown model message.

        :param message: message to be displayed
        :param model: model object
        :return: Unknown model message
        """
        classname = ""

        if model:
            classname = model.__class__.__name__

        super().__init__(f"Unknown model {classname}: \n {message}")


def __state_to_string__(state: DatamartState):
    """
    Function to print DataMart status

    :param DatamartState: State of the DataMart Object (Flask Document)
    :return: status
    """
    if state == DatamartState.RUNNING:
        return "running"
    elif state == DatamartState.SUCCESS:
        return "success"
    elif state == DatamartState.FAILED:
        return "failed"


def mapper(model):
    """
    Function to map models to data.
    Maps input model to desired dictionary object to allow acces of the stored data.
    All models can be found in data_access.models.

    :param model: Flask Document to be mapped to dictionary
    :return: dictionary object
    """
    if model is None:
        return None

    if type(model) is HTTPStatus:
        return model

    # ===== Workspace ==============================================================================
    if isinstance(model, Workspace):
        return {
            "id": str(model.id),
            "name": model.name
        }

    # ===== user ===================================================================================
    if isinstance(model, User):
        return {
            "email": model.email,
            "firstname": model.firstname,
            "lastname": model.lastname,
            "isAdmin": model.is_admin
        }

    # ===== annotation =============================================================================
    if isinstance(model, Annotation):
        return {
            "datamart_id": str(model.datamart_id.id),
            "data_attribute": model.data_attribute,
            "ontology_attribute": model.ontology_attribute,
            "comment": model.comment
        }

    # ===== datamart status ========================================================================
    if isinstance(model, DatamartStatus):
        return {
            "state": __state_to_string__(model.state),
            "started": model.started.isoformat() if model.started else None,
            "ended": model.ended.isoformat() if model.ended else None,
            "error": model.error
        }

    # ===== mongodb storage ========================================================================
    if isinstance(model, MongodbStorage):
        return {
            "datatype": model.datatype,
            "host": model.host,
            "port": model.port,
            "user": model.user,
            "database": model.database,
            "collection": model.collection
        }

    # ===== postgresql storage =====================================================================
    if isinstance(model, PostgresqlStorage):
        return {
            "datatype": model.datatype,
            "host": model.host,
            "port": model.port,
            "user": model.user,
            "database": model.database,
            "table": model.table
        }

    # ===== csv storage ============================================================================
    if isinstance(model, CsvStorage):
        return {
            "datatype": model.datatype,
            "mimetype": model.mimetype,
            "file": model.file,
            "hasHeader": model.has_header,
            "delimiter": model.delimiter
        }

    # ===== json storage ===========================================================================
    if isinstance(model, JsonStorage):
        return {
            "datatype": model.datatype,
            "mimetype": model.mimetype,
            "file": model.file
        }

    # ===== xml storage ============================================================================
    if isinstance(model, XmlStorage):
        return {
            "datatype": model.datatype,
            "mimetype": model.mimetype,
            "file": model.file,
            "rowTag": model.row_tag
        }

    # ===== metadata ===============================================================================
    if isinstance(model, Metadata):
        heritage = []
        try:
            for ancestor in model.heritage:
                heritage.append(mapper(ancestor.fetch()))
        except Exception as e:
            # If the any datamart from heritage is deleted, this will return except here
            print("Heritage datamart is not found")
            heritage = []

        return {
            "createdAt": model.created_at.isoformat() if model.created_by else None,
            "heritage": heritage,
            "constructionCode": model.construction_code,
            "constructionQuery": model.construction_query,
            "source": mapper(model.source),
            "target": mapper(model.target),
            "schema": json.loads(model.schema) if model.schema else ''
        }

    # ===== datamart ===============================================================================
    if isinstance(model, Datamart):
        return {
            "uid": model.uid,
            "humanReadableName": model.human_readable_name,
            "workspace_id": model.workspace_id,
            "comment": model.comment,
            "metadata": mapper(model.metadata),
            "status": mapper(model.status)
        }

    # ===== Ontology ===============================================================================
    if isinstance(model, Ontology):
        return {
            "id": str(model.id),
            "name": model.name,
            "workspace_id": str(model.workspace.id)
        }

    else:
        raise UnknownModel("couldn't turn model to dictionary", model)
