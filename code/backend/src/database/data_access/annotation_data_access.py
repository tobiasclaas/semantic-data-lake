from database.models.workspace import Workspace
from werkzeug.exceptions import NotFound, BadRequest
from database.models import Annotation


def get(workspace_id, file_name, data_attribute):
    """
    Get all annotations for data_attribute.
    :param workspace_id:
    :param file_name:
    :param data_attribute:
    :return:
    """
    pass


def add(workspace_id, file_name, data_attribute, ontology_attribute, comment=''):
    """
    Stores an annotation in MongoDB.
    :return:
    """

    # TODO check if workspace exists or get current workspace
    # TODO check if file exists
    # TODO check if file has attribute: data_attribute
    # TODO check if ontology_attribute exists in workspace
    print("Test")

    entity = Annotation(workspace_id=workspace_id, file_name=file_name, data_attribute=data_attribute,
                        ontology_attribute=ontology_attribute, comment=comment)
    Annotation.objects.insert(entity)

    # is it stored?

    return entity


def delete(workspace_id, file_name, data_attribute, ontology_attribute):
    """
    Delete annotation of ontology_attribute for data_attribute.
    :param workspace_id:
    :param file_name:
    :param data_attribute:
    :param ontology_attribute:
    :return:
    """
    pass


def delete_all(workspace_id, file_name):
    """
    Delete all annotations for a file.
    :param workspace_id:
    :param file_name:
    :return:
    """
    pass
